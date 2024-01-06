from fastapi import APIRouter, Body
from models.userModels import MainUser, MainUserdb, NewResponse
from typing import Union, Annotated

users_router = APIRouter()

users_list = [
    MainUserdb(name="Williams", id=42, password="**********"),
    MainUserdb(name="Davis", id=77, password="**********")
]


def password_encryption(code: str):
    result = code * 55


def find_user(identifier: int) -> Union[MainUserdb, None]:
    for user in users_list:
        if user.id == identifier:
            return user
    return None


@users_router.get("/api/users", response_model=Union[list[MainUser], None])
def get_users():
    """
    Получить список всех пользователей
    """
    return users_list


@users_router.get("/api/users/{id}", response_model=Union[MainUser, NewResponse])
def get_user(identifier: int):
    """
    Получить пользователя по его ID
    """
    user = find_user(identifier)
    print(user)
    if user is None:
        return NewResponse(message="Пользователь не был найден")
    return user


@users_router.post("/api/users", response_model=Union[MainUser, NewResponse])
def create_user(item: Annotated[MainUser, Body(embed=True, description="Новый пользователь")]):
    """
    Создание нового пользователя
    """
    user = MainUserdb(name=item.name, id=item.id, password=password_encryption(item.name))
    users_list.append(user)
    return user


@users_router.put("/api/users", response_model=Union[MainUser, NewResponse])
def edit_user(item: Annotated[MainUser, Body(embed=True, description="Изменение данных полльзователя по ID")]):
    """
    Обновление информации о пользователе
    """
    user = find_user(item.id)
    if user is None:
        return NewResponse(message="Пользователь не был найден")
    user.id = item.id
    user.name = item.name
    return user


@users_router.delete("/api/users/{id}", response_model=Union[list[MainUser], None])
def delete_user(identifier: int):
    """
    Удаление пользователя
    """
    user = find_user(identifier)
    if user is None:
        return NewResponse(message="Пользователь не был найден")
    users_list.remove(user)
    return users_list
