from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from api.users import users_router

app = FastAPI(
    version="0.1.1",
    description="Задание реализующее CRUD на FastAPI. Выполнил Скрипченко С.Д."
)

app.include_router(users_router, tags=["Users controller"])


@app.get("/", response_class=PlainTextResponse, tags=["Main controller"])
def root_page():
    return "Добро пожаловать!"
