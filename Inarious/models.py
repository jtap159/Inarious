from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    middle_name = Column(String)
    gender = Column(String)
