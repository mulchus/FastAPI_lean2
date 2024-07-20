from fastapi import FastAPI, Request, status

from contextlib import asynccontextmanager

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError

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


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"details": exc.errors()})
    )

app.include_router(tasks_router)
app.include_router(users_rourter)
app.include_router(null_router)
