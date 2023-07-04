from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    gender: str
