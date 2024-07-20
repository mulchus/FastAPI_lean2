from database import new_session
from schemas import STaskAdd, STask
from sqlalchemy import select

from database import TasksOrm


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TasksOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas

    @classmethod
    async def find_by_id(cls, task_id: int) -> STask:
        async with new_session() as session:
            query = select(TasksOrm).where(TasksOrm.id == task_id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            task_schema = STask.model_validate(task_model)
            return task_schema
