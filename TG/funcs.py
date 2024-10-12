import asyncio

import aiohttp
import aioredis
import json

from config import config


# Функция для получения погоды из OpenWeatherMap
async def fetch_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": config.API_KEY,
        "units": "metric",  # Используем метрические единицы (Celsius)
        "lang": "ru"        # Русский язык для описания погоды
    }
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def init_redis():
    # Инициализация Redis
    redis = await aioredis.from_url("redis://localhost")
    return redis


async def main():
    redis = await init_redis()
    # Здесь вы можете использовать redis для кэширования данных
    await redis.set("key", "value")
    value = await redis.get("key")
    print(value)  # Должно вывести: b'value'
    await redis.close()  # Закрываем соединение

if __name__ == "__main__":
    asyncio.run(main())