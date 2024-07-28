from httpx import AsyncClient
import pytest
from datetime import datetime


@pytest.fixture(scope="session")
async def add_first_operation(ac: AsyncClient):
    await ac.post("/operations/", json={
        "id": 1,
        "quantity": "100",
        "figi": "fixture",
        "instrument_type": "share",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        "type": "выплата купонов",
    })


@pytest.mark.asyncio(scope="session")
async def test_add_specific_operations(ac: AsyncClient, add_first_operation):
    response = await ac.post("/operations/", json={
        "id": 2,
        "quantity": "10",
        "figi": "BBG000B9XRY4",
        "instrument_type": "share",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        "type": "выплата купонов",
    })
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations/", params=({"operation_type": "выплата купонов"}))
    print(response.json())
    assert response.json()['data'][0]['type'] == "выплата купонов"
    assert len(response.json()['data']) == 2
