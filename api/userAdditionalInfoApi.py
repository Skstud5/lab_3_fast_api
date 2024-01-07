from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.userModels import UserAdditionalInfoEntity, UserAdditionalInfo
from data_base.data_base import get_session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

user_additional_info_router = APIRouter(tags=[Tags.user_additional_info], prefix='/api/user/addInfo')


def password_encryption(password: str):
    return pbkdf2_sha256.hash(password)


@user_additional_info_router.get("/", response_model=List[UserAdditionalInfo])
async def get_all_additional_user_info(user_id: int, data_base: Session = Depends(get_session)):
    """
    Получить все записи дополнительной информации о пользователе по ID
    """
    async with data_base.begin():
        query = select(UserAdditionalInfoEntity).filter(UserAdditionalInfoEntity.id_user == user_id)
        final_data = await data_base.execute(query)
        user_additional_info = final_data.scalars().all()

    if user_additional_info is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return user_additional_info


@user_additional_info_router.get("/{id}", response_model=UserAdditionalInfo)
async def get_additional_user_info(identifier: int, data_base: Session = Depends(get_session)):
    """
    Получить дополнительную информацию о пользователе по ID
    """
    async with data_base.begin():
        query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
        final_data = await data_base.execute(query)
        user_additional_info = final_data.scalar()

    if user_additional_info is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return user_additional_info


@user_additional_info_router.post("/", response_model=UserAdditionalInfo)
async def create_additional_info(cr_user: UserAdditionalInfo, data_base: AsyncSession = Depends(get_session)):
    """
    Создать дополнительную информация для пользователя
    """
    try:
        user_additional_info = UserAdditionalInfoEntity(id_user=cr_user.id_user, data=cr_user.data)
        if user_additional_info is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with data_base.begin():
            data_base.add(user_additional_info)
            await data_base.commit()

        await data_base.refresh(user_additional_info)
        result = UserAdditionalInfoEntity(id=user_additional_info.id,
                                          id_user=user_additional_info.id_user,
                                          data=user_additional_info.data)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_user}")


@user_additional_info_router.delete("/", response_model=UserAdditionalInfo)
async def delete_additional_info(identifier: int, data_base: AsyncSession = Depends(get_session)):
    """
    Удалить дополнительную информация для пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
            result = await data_base.execute(query)
            user_additional_info = result.scalar()

            if user_additional_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(user_additional_info)

        return user_additional_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@user_additional_info_router.put("/{id}", response_model=UserAdditionalInfo)
async def update_user_additional_info(identifier: int, updated_info: UserAdditionalInfo,
                                      data_base: AsyncSession = Depends(get_session)):
    """
    Полное обновление дополнительной информации для пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id_user = updated_info.id_user
            existing_info.data = updated_info.data

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@user_additional_info_router.patch("/{id}", response_model=UserAdditionalInfo)
async def partial_update_user_additional_info(identifier: int, updated_info: UserAdditionalInfo,
                                              data_base: AsyncSession = Depends(get_session)):
    """
    Частичное обновление дополнительной информации для пользователя
    """
    try:
        async with data_base.begin():
            query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id_user:
                existing_info.id_user = updated_info.id_user
            if updated_info.data:
                existing_info.data = updated_info.data

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
