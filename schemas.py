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
    currency: str = Field(in_=["USD", "EUR", "GBP"])
    side: str
    price: float = Field(ge=0)
    amount: float

    # model_config = ConfigDict(from_attributes=True)
