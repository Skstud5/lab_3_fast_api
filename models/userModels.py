from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl


class Photo(BaseModel):
    url: HttpUrl
    name: Union[str, None] = None


class Person(BaseModel):
    name: str = Field(default="Фамилия", min_legth=3, max_length=20)
    age: int = Field(default=100, ge=10, lt=200)


class User(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=10, lt=200)] = None
    person: Union[Person, None] = None
    day_list0: list
    day_list1: Union[list, None] = None
    day_list2: Union[list[int], None] = None
    foto_list: Union[list[Photo], None] = None


class MainUser(BaseModel):
    name: Union[str, None] = None
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None


class MainUserdb(MainUser):
    password: Annotated[Union[str, None], Field(max_length=200, min_length=8)] = None


class NewResponse(BaseModel):
    message: str
