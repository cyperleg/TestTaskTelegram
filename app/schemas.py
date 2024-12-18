import re
from pydantic import BaseModel, ConfigDict, field_validator, Field
from typing import Union, Optional, Annotated


class BaseModelORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HashPassword(BaseModel):
    hash_password: str

    @field_validator('hash_password')
    def validate_api_id(cls, value):
        if len(value) > 62 or len(value) < 58:
            raise ValueError("Hash is corrupted")
        return value


class APITelegram(BaseModel):
    api_id: int
    api_hash: str
    phone_number: str

    @field_validator('api_id')
    def validate_api_id(cls, value):
        if value <= 0:
            raise ValueError("API ID must be a positive integer.")
        return value

    @field_validator('api_hash')
    def validate_api_hash(cls, value):
        if len(value) != 32:
            raise ValueError("API Hash must be exactly 32 characters long.")
        if not re.match(r"^[a-fA-F0-9]{32}$", value):
            raise ValueError("API Hash must contain only hexadecimal characters (0-9, a-f).")
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if not re.match(r"^\+?[0-9]\d{9,14}$", value):
            raise ValueError("Phone number must contain sign + and numbers")
        return value


class UserIn(BaseModelORM):
    login: str
    password: Union[str, HashPassword]

    @field_validator('login')
    def validate_login(cls, value):
        if 8 > len(value) or len(value) > 20:
            raise ValueError("Login must be between 8 and 20 characters.")
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValueError("Login can only contain letters, numbers, dots, underscores, and dashes.")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if isinstance(value, str):
            if 8 > len(value) or len(value) > 20:
                raise ValueError("Password must be between 8 and 20 characters")
            if not any(char.isdigit() for char in value):
                raise ValueError("Password must contain at least one digit.")
            if not any(char.isalpha() for char in value):
                raise ValueError("Password must contain at least one letter.")
            if not re.search(r"[!@#$%^&*()\-_=+]", value):
                raise ValueError("Password must contain at least one special character (!@#$%^&*()-_+=).")
        return value


class User(UserIn):
    id: Annotated[Optional[int], Field(exclude=True)] = None
    api: Optional[APITelegram] = None
    hash_phone: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class DialogSchema(BaseModel):
    name: str
    identification: int


class APICode(BaseModel):
    code: int

    @field_validator('code')
    def validate_code(cls, value):
        if len(str(value)) != 5:
            raise ValueError("Code must be exactly 5 digits")
        return value
