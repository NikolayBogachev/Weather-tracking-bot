import pytest

from tests.initdb import create_data_1, create_data_2, create_data_3


@pytest.mark.asyncio
async def test_unfollow_user(client, setup_database):
    await create_data_1()
    response = await client.get("/logs")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['command'] == '/weather Moscow'

@pytest.mark.asyncio
async def test_get_logs_by_user(client, setup_database):
    user_id = 1
    await create_data_2(user_id)

    response = await client.get(f"/logs/{user_id}")

    assert response.status_code == 200

    logs = response.json()
    assert isinstance(logs, list)
    assert len(logs) == 1  # Проверка на количество логов
    assert logs[0]['user_id'] == user_id
    assert logs[0]['command'] == "test_command"
    assert logs[0]['response'] == "test_response"

@pytest.mark.asyncio
async def test_get_logs_by_user_with_dates(client,setup_database):
    user_id = 1
    await create_data_3(user_id)

    response = await client.get(f"/logs/{user_id}?start_date=2024-10-01&end_date=2024-10-02")

    assert response.status_code == 200

    logs = response.json()
    assert isinstance(logs, list)
    assert len(logs) == 2