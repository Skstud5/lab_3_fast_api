from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.userModels import User, UserEntity
from data_base.data_base import get_session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

users_router = APIRouter(tags=[Tags.users], prefix='/api/users')


def password_encryption(password: str):
    return pbkdf2_sha256.hash(password)


@users_router.get("/", response_model=List[User])
async def get_all_users(data_base: Session = Depends(get_session)):
    """
    Получить всех пользователей
    """
    async with data_base.begin():
        query = select(UserEntity)
        final_data = await data_base.execute(query)
        user_additional_info = final_data.scalars().all()

    if user_additional_info is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return user_additional_info


@users_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, data_base: Session = Depends(get_session)):
    """
    Получить пользователя по его ID
    """
    async with data_base.begin():
        query = select(UserEntity).where(UserEntity.id == user_id)
        final_data = await data_base.execute(query)
        user = final_data.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@users_router.post("/", response_model=User)
async def create_user(cr_user: User, database: AsyncSession = Depends(get_session)):
    """
    Создать пользователя
    """
    try:
        hashed_password = password_encryption(cr_user.hash_password)
        user = UserEntity(name=cr_user.name, hash_password=hashed_password)

        async with database.begin():
            database.add(user)
            await database.commit()

        # Обновляем объект пользователя, чтобы получить его ID
        await database.refresh(user)

        result = User(id=user.id, name=user.name, hash_password=user.hash_password)

        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении пользователя: {exc}")


@users_router.delete("/", response_model=User)
async def delete_user(identifier: int, data_base: AsyncSession = Depends(get_session)):
    """
    Удалить пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            user_additional_info = result.scalar()

            if user_additional_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(user_additional_info)

        return user_additional_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@users_router.put("/{id}", response_model=User)
async def update_user_additional_info(identifier: int, updated_info: User,
                                      data_base: AsyncSession = Depends(get_session)):
    """
    Полное обновление пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.name = updated_info.name
            existing_info.hash_password = password_encryption(updated_info.hash_password)

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@users_router.patch("/{id}", response_model=User)
async def partial_update_user_additional_info(identifier: int, updated_info: User,
                                              data_base: AsyncSession = Depends(get_session)):
    """
    Частичное обновление пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.name:
                existing_info.name = updated_info.name
            if updated_info.hash_password:
                existing_info.hash_password = password_encryption(updated_info.hash_password)

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
