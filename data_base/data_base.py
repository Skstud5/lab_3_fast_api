import asyncio
from config.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URI_ASYNC = "postgresql+asyncpg://adminMovie:5806719824@localhost:5455/movies"

URI_SYNC = settings.DATABASE_URL_SYNC
URI_ASYNC = settings.DATABASE_URL_ASYNC

print(URI_SYNC)
print(URI_ASYNC)
print(DATABASE_URI_ASYNC)

engine = create_async_engine(URI_ASYNC, echo=True)


async def connect_to_database():
    async with engine.connect() as connection:
        result = await connection.execute(text("select version()"))
        print(f"answer = {result.all()}")


asyncio.run(connect_to_database())
