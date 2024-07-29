from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Annotated

from src.task.repository import TaskRepository
from src.task.schemas import STaskAdd, STask, STaskID, Trade, User

from src.task.database import fake_users, fake_trades

from src.auth.base_config import current_user

from src.task.tasks import send_email_report_dashboard


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


@tasks_router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # 1400 ms - Клиент ждет
    send_email_report_dashboard(user.username)
    # 500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    background_tasks.add_task(send_email_report_dashboard, user.username, "var.2")
    # 600 ms - Задача выполняется воркером Celery в отдельном процессе
    send_email_report_dashboard.delay(user.username, "var.3")
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }


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


@users_rourter.get("/{user_id}", response_model=list[User])
async def get_user(user_id: int) -> list[dict]:
    return [user for user in fake_users if user.get("id") == user_id]


@null_router.post("/trades")
def add_trade(trades: list[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "trades": fake_trades}
