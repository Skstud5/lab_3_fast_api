from pydantic import BaseModel
from enum import Enum


class Tags(Enum):
    users = "users"
    movies = "movies"
    info = "info"


class NewResponse(BaseModel):
    message: str
