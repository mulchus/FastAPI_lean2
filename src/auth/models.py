from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, metadata


role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(128), nullable=False),
    Column('permissions', JSON)
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(128), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
    Column('role_id', Integer, ForeignKey(role.c.id)),
    Column('email', String(128), nullable=False),
    Column('hashed_password', String(1024), nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow())
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(role.c.id))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
