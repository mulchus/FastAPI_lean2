from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables
from router import tasks_router, users_rourter, null_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Создание таблиц')
    yield
    print('Завершение работы')


app = FastAPI(
    title='Task Manager',
    lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(users_rourter)
app.include_router(null_router)


