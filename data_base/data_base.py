import asyncio
from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from config.config import settings
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from models.movies import Base
from models.generalModels import Tags
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from models.userModels import User, UserEntity

engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

users_router = APIRouter(tags=[Tags.users], prefix='/api/users')


async def init_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserEntity))
        data = result.fetchall()
        print(data)

# async def init_db():
#     Base.metadata.create_all(bind=engine_async)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
