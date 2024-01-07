from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_sequence"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hash_password = Column(String)


class UserAdditionalInfoEntity(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    data = Column(String)


class UserAdditionalInfo(BaseModel):
    id: int
    id_user: int
    data: str


class User(BaseModel):
    id: int
    name: str
    hash_password: str
