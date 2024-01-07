from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.moviesModels import DirectorEntity, Director
from data_base.data_base import get_session
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

directors_router = APIRouter(tags=[Tags.directors], prefix='/api/directors')


@directors_router.get("/", response_model=List[Director])
async def get_all_directors(data_base: Session = Depends(get_session)):
    """
    Получить всех режиссеров
    """
    async with data_base.begin():
        query = select(DirectorEntity)
        final_data = await data_base.execute(query)
        movies = final_data.scalars().all()

    if movies is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return movies


@directors_router.get("/{id}", response_model=Director)
async def get_director(identifier: int, data_base: Session = Depends(get_session)):
    """
    Получить режиссера по ID
    """
    async with data_base.begin():
        query = select(DirectorEntity).where(DirectorEntity.id == identifier)
        final_data = await data_base.execute(query)
        movie = final_data.scalar()

    if movie is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return movie


import logging


@directors_router.post("/", response_model=Director)
async def create_director(cr_director: Director, data_base: AsyncSession = Depends(get_session)):
    """
    Создать режиссера
    """
    try:
        director = DirectorEntity(
            name=cr_director.name,
            birth_date=cr_director.birth_date,
            country=cr_director.country
        )
        if director is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with data_base.begin():
            data_base.add(director)
            await data_base.commit()

        await data_base.refresh(director)
        result = Director(name=director.name, birth_date=director.birth_date, country=director.country)
        return result
    except Exception as exc:
        logging.error(f"Error while adding movie: {exc}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_director}")


@directors_router.delete("/", response_model=Director)
async def delete_director(identifier: int, data_base: AsyncSession = Depends(get_session)):
    """
    Удалить режиссера
    """
    try:
        async with data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await data_base.execute(query)
            director = result.scalar()

            if director is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(director)

        return director
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@directors_router.put("/{id}", response_model=Director)
async def update_director(identifier: int, updated_info: Director,
                          data_base: AsyncSession = Depends(get_session)):
    """
    Полное обновление режиссера
    """
    try:
        async with data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.name = updated_info.name
            existing_info.birth_date = updated_info.birth_date
            existing_info.country = updated_info.country

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@directors_router.patch("/{id}", response_model=Director)
async def partial_update_director(identifier: int, updated_info: Director,
                                  data_base: AsyncSession = Depends(get_session)):
    """
    Частичное обновление режиссера
    """
    try:
        async with data_base.begin():
            query = select(DirectorEntity).where(DirectorEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.name:
                existing_info.name = updated_info.name
            if updated_info.birth_date:
                existing_info.birth_date = updated_info.birth_date
            if updated_info.country:
                existing_info.country = updated_info.country

        return existing_info
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
