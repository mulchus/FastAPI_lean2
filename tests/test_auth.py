import pytest
import time
from sqlalchemy import insert, select

from src.auth.models import role
from conftest import client, async_session_maker


@pytest.mark.asyncio(scope="session")
async def test_add_role():
    print("\ntest_add_role")
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        roles = result.all()
        print(roles)
        # assert len(roles) == 1
        assert roles == [(1, 'admin', None)], "Не создались все роли"


def test_register():
    responce = client.post('/auth/register', json={
        "email": "test@ya.ru",
        "username": "test",
        "password": "test",
        "role_id": 1,
        "created_at": time.time(),
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    })

    print(responce.json())
    assert responce.status_code == 201
    assert responce.json()['email'] == 'test@ya.ru'
