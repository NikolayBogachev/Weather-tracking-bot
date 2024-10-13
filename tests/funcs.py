import asyncio
import sys

import aiohttp
import aioredis
import json


from loguru import logger

from config import config

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")

CACHE_TTL = 600  # Время жизни кэша (10 минут)
MAX_RETRIES = 5  # Максимальное количество попыток
RETRY_DELAY = 2  # Начальная задержка перед повторной попыткой (в секундах)


# Функция для получения погоды из OpenWeatherMap
async def fetch_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": config.API_KEY,
        "units": "metric",  # Используем метрические единицы (Celsius)
        "lang": "ru"        # Русский язык для описания погоды
    }
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(base_url, params=params) as response:
            print(f"Fetching weather for: {city_name}, Response status: {response.status}")  # Логируем статус ответа
            if response.status == 200:
                return await response.json()
            else:
                return None


async def fetch_weather_with_cache(city_name: str, bot, message, redis):
    """
    Получает погоду из кэша или из внешнего API, если кэш отсутствует или устарел.
    """
    if redis is None:
        logger.error("Объект redis равен None!")
        return None
    # Проверка наличия кэшированных данных в Redis
    cached_weather = await redis.get(f"weather:{city_name.lower()}")

    if cached_weather:
        # Декодирование кэшированных данных
        weather_data = json.loads(cached_weather)
        logger.info(f"Возвращаю погоду для {city_name} из кэша.")
        return weather_data

    # Если данных в кэше нет, делаем запрос в внешний API с повторными попытками
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            # Запрос к внешнему API
            weather_data = await fetch_weather(city_name)

            if weather_data:
                # Кэшируем данные погоды на 10 минут
                await redis.set(f"weather:{city_name.lower()}", json.dumps(weather_data), ex=CACHE_TTL)
                logger.info(f"Погода для {city_name} закэширована.")
                return weather_data

            logger.warning(f"Не удалось получить погоду для {city_name}.")
            return None

        except aiohttp.ClientOSError as e:
            attempt += 1
            logger.error(f"Ошибка соединения с API для {city_name}: {e}. Попытка {attempt}/{MAX_RETRIES}.")


