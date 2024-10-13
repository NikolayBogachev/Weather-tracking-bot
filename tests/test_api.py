import pytest
from httpx import AsyncClient
from main import app  # предполагается, что FastAPI приложение находится в main.py

@pytest.mark.asyncio
async def test_get_logs(mocker):
    # Мокаем вызов к базе данных
    mocker.patch('api.handlers.get_logs', return_value=[
        {'user_id': 1, 'command': '/weather Moscow', 'response': 'Погода в Москве...', 'created_at': '2024-01-01T12:00:00'}
    ])

    async with AsyncClient(app=app, base_url="http://test.database") as ac:
        response = await ac.get("/logs")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['command'] == '/weather Moscow'