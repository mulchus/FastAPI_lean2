from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()


roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(128), nullable=False),
    Column('permissions', JSON)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String(128), nullable=False),
    Column('username', String(128), nullable=False),
    Column('password', String(128), nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow()),
    Column('role_id', Integer, ForeignKey('roles.id')),
)



