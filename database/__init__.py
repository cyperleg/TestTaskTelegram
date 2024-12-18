from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from sqlalchemy.orm import Session
from config import DB_LOCATION, DB_NAME


db_engine = create_engine(DB_LOCATION)


# Creating database file if not existed
def database_create():
    _engine = create_engine(f"sqlite:///{DB_NAME}.db", echo=True)
    if not database_exists(_engine.url):
        print(f"Database file within path {_engine.url} not found. Creating database file {DB_LOCATION}")
        try:
            Base.metadata.create_all(_engine)
            print(f"Database created")
        except Exception as e:
            print(f"Error occered: \n {e}")


def create_test_data():
    with Session(db_engine) as session:
        user = User(login="Test", password="121212")
        session.add(user)
        session.commit()


if __name__ == "__main__":
    from database import Base, User
    print(DB_LOCATION)

    database_create()
    create_test_data()
