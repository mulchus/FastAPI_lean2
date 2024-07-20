from fastapi import APIRouter, Depends
from typing import Annotated

from repository import TaskRepository
from schemas import STaskAdd, STask, STaskID, Trade

from database import fake_users, fake_trades

tasks_router = APIRouter(
    tags=["Tasks"],
    prefix="/tasks"
)

users_rourter = APIRouter(
    tags=["Users"],
    prefix="/users"
)

null_router = APIRouter(
    tags=["Default"],
    prefix=""
)


@tasks_router.post("")
async def add_task(
        task: Annotated[STaskAdd, Depends()],
) -> STaskID:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@tasks_router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    print(tasks)
    return tasks


@tasks_router.get("/{task_id}")
async def get_task(task_id: int) -> STask:
    task = await TaskRepository.find_by_id(task_id)
    return task


@users_rourter.get("/{user_id}")
async def get_user(user_id: int) -> list[dict]:
    return [user for user in fake_users if user.get("id") == user_id]


@null_router.post("/trades")
def add_trade(trades: list[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "trades": fake_trades}
