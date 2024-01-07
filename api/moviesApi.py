from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.generalModels import Tags
from models.moviesModels import MovieEntity, Movie, DirectorEntity, Director
from data_base.data_base import get_session
from fastapi import HTTPException
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

movies_router = APIRouter(tags=[Tags.movies], prefix='/api/movies')


@movies_router.get("/", response_model=List[Movie])
async def get_all_movies(data_base: Session = Depends(get_session)):
    """
    Получить все фильмы
    """
    async with data_base.begin():
        query = select(MovieEntity)
        final_data = await data_base.execute(query)
        movies = final_data.scalars().all()

    if movies is None:
        raise HTTPException(status_code=404, detail="Записи не найдены")
    return movies


@movies_router.get("/{id}", response_model=Movie)
async def get_movie(identifier: int, data_base: Session = Depends(get_session)):
    """
    Получить фильм по ID
    """
    async with data_base.begin():
        query = select(MovieEntity).where(MovieEntity.id == identifier)
        final_data = await data_base.execute(query)
        movie = final_data.scalar()

    if movie is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return movie


import logging


@movies_router.post("/", response_model=Movie)
async def create_movie(cr_movie: Movie, data_base: AsyncSession = Depends(get_session)):
    """
    Создать пользователя
    """
    try:
        movie = MovieEntity(
            title=cr_movie.title,
            release_year=cr_movie.release_year,
            genre=cr_movie.genre,
            rating=cr_movie.rating,
            is_published=cr_movie.is_published,
            director_id=cr_movie.director_id
        )
        if movie is None:
            raise HTTPException(status_code=404, detail="Объект не определен")

        async with data_base.begin():
            data_base.add(movie)
            await data_base.commit()

        await data_base.refresh(movie)
        result = Movie(id=movie.id,
                       title=movie.title,
                       release_year=movie.release_year,
                       genre=movie.genre,
                       rating=movie.rating,
                       is_published=movie.is_published,
                       director_id=movie.director_id
                       )
        return result
    except Exception as exc:
        logging.error(f"Error while adding movie: {exc}")
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_movie}")


@movies_router.delete("/", response_model=Movie)
async def delete_movie(identifier: int, data_base: AsyncSession = Depends(get_session)):
    """
    Удалить фильм
    """
    try:
        async with data_base.begin():
            query = select(MovieEntity).where(MovieEntity.id == identifier)
            result = await data_base.execute(query)
            movie = result.scalar()

            if movie is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(movie)

        return movie
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")

# @movies_router.put("/{id}", response_model=UserAdditionalInfo)
# async def update_user_additional_info(identifier: int, updated_info: UserAdditionalInfo,
#                                       data_base: AsyncSession = Depends(get_session)):
#     """
#     Полное обновление дополнительной информации для пользователя
#     """
#     try:
#         async with data_base.begin():
#             query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
#             result = await data_base.execute(query)
#             existing_info = result.scalar()
#
#             if existing_info is None:
#                 raise HTTPException(status_code=404, detail="Запись не найдена")
#
#             existing_info.id_user = updated_info.id_user
#             existing_info.data = updated_info.data
#
#         return existing_info
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")
#
#
# @movies_router.patch("/{id}", response_model=UserAdditionalInfo)
# async def partial_update_user_additional_info(identifier: int, updated_info: UserAdditionalInfo,
#                                               data_base: AsyncSession = Depends(get_session)):
#     """
#     Частичное обновление дополнительной информации для пользователя
#     """
#     try:
#         async with data_base.begin():
#             query = select(UserAdditionalInfoEntity).where(UserAdditionalInfoEntity.id == identifier)
#             result = await data_base.execute(query)
#             existing_info = result.scalar()
#
#             if existing_info is None:
#                 raise HTTPException(status_code=404, detail="Запись не найдена")
#
#             if updated_info.id_user:
#                 existing_info.id_user = updated_info.id_user
#             if updated_info.data:
#                 existing_info.data = updated_info.data
#
#         return existing_info
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
