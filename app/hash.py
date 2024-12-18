from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    @staticmethod
    def hash(value: str) -> str:
        return pwd_context.hash(value)

    @staticmethod
    def validate(value: str, hash_value: str) -> bool:
        return pwd_context.verify(value, hash_value)
