from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(
    "sqlite+aiosqlite:///src\\task\\tasks.db",
    echo=True
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TasksOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


fake_tasks = [
    {"id": 1, "name": "Task 1", "description": "Description 1"},
    {"id": 2, "name": "Task 2", "description": "Description 2"},
    {"id": 3, "name": "Task 3", "description": "Description 3"},
]

fake_users = [
    {"id": 1, "role": "admin", "name": "User 1",
     "deeges": [{"id": 1, "created_at": "2022-01-01T00:00:00", "type_deegrees": "expert"},]
     },
    {"id": 2, "role": "user", "name": "User 2",
     "deeges": [{"id": 2, "created_at": "2022-01-01T00:00:00", "type_deegrees": "newbie"}]},
    {"id": 3, "role": "user", "name": "User 3"},    # опционально
]

fake_trades = [
    {"id": 1, "user_id": 1, "currency": "USD", "side": "buy", "price": 100, "amount": 10},
    {"id": 2, "user_id": 2, "currency": "EUR", "side": "sell", "price": 200, "amount": 20},
    {"id": 3, "user_id": 2, "currency": "GBP", "side": "buy", "price": 300, "amount": 30},
]
