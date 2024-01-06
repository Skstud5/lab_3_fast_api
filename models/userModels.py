from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_sequence"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hash_password = Column(String)


class User(BaseModel):
    id: int
    name: str
    hash_password: str


class Photo(BaseModel):
    url: HttpUrl
    name: Union[str, None] = None


class MainUser(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
