from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.userModels import User, UserEntity
from data_base.data_base import get_session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter(tags=[Tags.users], prefix='/api/users')


def password_encryption(password: str):
    return pbkdf2_sha256.hash(password)


@users_router.get("/{id}", response_model=User)
async def get_user(user_id: int, data_base: Session = Depends(get_session)):
    """
    Получить пользователя по его ID
    """
    async with data_base.begin():
        query = select(UserEntity).where(UserEntity.id == user_id)
        result = await data_base.execute(query)
        user = result.scalar()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@users_router.post("/", response_model=User)
async def create_user(cr_user: User, data_base: AsyncSession = Depends(get_session)):
    try:
        user = UserEntity(name=cr_user.name, hash_password=password_encryption(cr_user.name))
        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with data_base.begin():
            data_base.add(user)
            await data_base.commit()

        await data_base.refresh(user)
        result = User(id=user.id, name=user.name, hash_password=user.hash_password)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_user}")
