from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from src.database import metadata


operation = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP(timezone=True)),
    Column("type", String),
)
