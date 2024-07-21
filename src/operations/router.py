from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

operation_router = APIRouter(
    prefix="/operations",
    tags=["Operations"]
)


@operation_router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    print(query)
    result = await session.execute(query)
    return result.all()


@operation_router.post("/")
async def add_specific_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    # stmt = operation.insert().values(**new_operation.dict())
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'ok'}
