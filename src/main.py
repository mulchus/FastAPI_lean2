from fastapi import FastAPI, Request, status

from contextlib import asynccontextmanager

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from collections.abc import AsyncIterator
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from redis import asyncio as aioredis

from src.config import REDIS_HOST, REDIS_PORT
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import operation_router
from src.pages.router import pages_router
from src.task.database import create_tables
from src.task.router import tasks_router, users_rourter, null_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    await create_tables()
    print('Создание таблиц')
    yield
    print('Завершение работы')


app = FastAPI(
    title='FastAPI Manager',
    lifespan=lifespan)


# app.add_middleware(HTTPSRedirectMiddleware)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(tasks_router)
app.include_router(users_rourter)
app.include_router(null_router)
app.include_router(operation_router)
app.include_router(pages_router)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"details": exc.errors()})
    )


@app.on_event("startup")
async def startup_event() -> None:
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown() -> None:
    await fastapi_users.close_redis()
