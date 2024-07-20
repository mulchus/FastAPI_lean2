from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class STaskID(BaseModel):
    ok: bool
    task_id: int


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(min_length=3, max_length=3)
    side: str
    price: float = Field(ge=0)
    amount: float


class DeegreType(Enum):
    newbie = "newbie"
    intermediate = "intermediate"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_deegrees: DeegreType


class User(BaseModel):
    id: int
    role: str
    name: str
    deeges: list[Degree]
