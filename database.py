from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum
from sqlmodel import Field, SQLModel, create_engine


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default=uuid4(), primary_key=True)
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Gender
    roles: List[Role]


psql_db = "fastapi"
psql_url = f"postgresql://postgres:mypass@127.0.0.1:5432/{psql_db}"

engine = create_engine(psql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
