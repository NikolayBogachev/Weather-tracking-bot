

import pytest
from unittest.mock import AsyncMock

from aioresponses import aioresponses

from handlers_bot import get_weather


@pytest.fixture
def mock_bot(mocker):
    """Создает мок для бота."""
    return mocker.Mock()


@pytest.fixture
def mock_message():
    message = AsyncMock()
    message.reply = AsyncMock()  # Мок метода reply
    message.from_user.id = 123  # Установите ID пользователя
    message.text = "/weather"  # Установите текст сообщения
    return message


@pytest.fixture
def mock_database():
    """Фикстура для мока базы данных."""
    db = AsyncMock()
    return db


@pytest.fixture
def mock_redis():
    """Фикстура для мока Redis."""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)  # Настройка возврата для get
    return redis

@pytest.mark.asyncio
async def test_get_weather_with_saved_city(mock_message, mock_database, mock_redis):
    """Тестирование получения погоды с сохранённым городом."""
    mock_database.get_user_city.return_value = "Москва"

    mock_bot = AsyncMock()  # Мок для бота

    with aioresponses() as m:
        m.get("http://api.openweathermap.org/data/2.5/weather", payload={
            "main": {"temp": 20, "feels_like": 18, "humidity": 50},
            "weather": [{"description": "ясно"}],
            "wind": {"speed": 5}
        })

        await get_weather(mock_message, mock_bot, mock_redis)


@pytest.mark.asyncio
async def test_get_weather_invalid_city(mock_message, mock_database, mock_redis):
    """Тестирование ввода некорректного названия города."""
    mock_message.text = "/weather 1234"

    await get_weather(mock_message, mock_bot, mock_redis)


@pytest.mark.asyncio
async def test_get_weather_no_city(mock_message, mock_database,  mock_redis):
    """Тестирование случая, когда пользователь не указал город."""
    mock_message.text = "/weather"

    await get_weather(mock_message, mock_bot, mock_redis)


@pytest.mark.asyncio
async def test_get_weather_city_not_found(mock_message, mock_database, mock_redis):
    """Тестирование случая, когда город не найден."""
    mock_database.get_user_city.return_value = "Город"

    with aioresponses() as m:
        m.get("http://api.openweathermap.org/data/2.5/weather", status=404)

        await get_weather(mock_message, mock_bot, mock_redis)

