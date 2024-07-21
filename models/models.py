from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()


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
    Column('email', String(128), nullable=False),
    Column('username', String(128), nullable=False),
    Column('hashed_password', String(1024), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
    Column('role_id', Integer, ForeignKey(role.c.id)),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)
