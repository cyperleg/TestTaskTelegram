from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Text


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_id = mapped_column(Integer, primary_key=True, unique=True)
    login = mapped_column(String, unique=True)
    password = mapped_column(Text)
    api_id = mapped_column(Integer, unique=True)
    api_hash = mapped_column(Text, unique=True)
    phone_number = mapped_column(String, unique=True)
    hash_phone = mapped_column(String, unique=True)

    def __repr__(self):
        return ("------------------------USER------------------------\n" +
                f"User id: {self.user_id}\n" +
                f"User login: {self.login}\n" +
                f"User password: {self.password}\n" +
                f"User api id: {self.api_id}\n" +
                f"User api hash: {self.api_hash}\n" +
                f"User phone number: {self.phone_number}\n" +
                f"User hash phone: {self.hash_phone}\n" +
                "-----------------------------------------------------")
