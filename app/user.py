from database import db_engine, Session
from database.database import User as User_DB
from app.schemas import User, UserIn, APITelegram
from sqlalchemy import select
from app.hash import HashPassword


class UserDAL:
    db = Session(db_engine)

    @classmethod
    def create_user(cls, user: UserIn):
        with cls.db as db:
            if db.execute(select(User_DB).where(User_DB.login == user.login)).scalar_one_or_none():
                print(db.execute(select(User_DB).where(User_DB.login == user.login)).scalar_one_or_none())
                raise ValueError("Nickname already exist")
            user = User_DB(login=user.login, password=HashPassword.hash(user.password), api_hash=None, api_id=None,
                           phone_number=None, hash_phone=None)
            db.add(user)
            db.commit()

    @classmethod
    def update_account(cls, user: User):
        with cls.db as db:
            extracted_user = db.execute(select(User_DB).where(User_DB.login == user.login)).scalar_one_or_none()
            if extracted_user:
                extracted_user.api_hash = user.api.api_hash
                extracted_user.api_id = user.api.api_id
                extracted_user.phone_number = user.api.phone_number
                extracted_user.hash_phone = user.hash_phone
                db.add(extracted_user)
                db.commit()
            else:
                raise ValueError("User not found")

    @classmethod
    def get_user_by_name(cls, name: str):
        with cls.db as db:
            extracted_user = db.execute(select(User_DB).where(User_DB.login == name)).scalar_one_or_none()
            if extracted_user:
                return extracted_user
            else:
                raise ValueError("User not found")

    @classmethod
    def get_user(cls, user: User):
        with cls.db as db:
            extracted_user = db.execute(select(User_DB).where(User_DB.login == user.login)).scalar_one_or_none()
            if extracted_user:
                if HashPassword.validate(user.password, extracted_user.password):
                    return extracted_user
                else:
                    raise ValueError("Password doesn't match")
            else:
                raise ValueError("User not found")


if __name__ == "__main__":
    name = "TEST1TEST"
    password = "TESTTesr_2"
    api_id = 1
    api_hash = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    phone_number = "+380992342344"
    hash_phone = "asdasdqwdqwdsadasdasdqwdqwdsadss"
    UserDAL.create_user(User(login=name, password=password))

    UserDAL.update_account(User(login=name, password=password, hash_phone=hash_phone,
                                api=APITelegram(api_id=api_id, api_hash=api_hash, phone_number=phone_number)))
