from pydantic import BaseModel
from enum import Enum


class Tags(Enum):
    main = "Main Controller"
    users = "Users"
    movies = "Movies"
    directors = "Directors"
    user_additional_info = "User Additional Info"


class NewResponse(BaseModel):
    message: str
