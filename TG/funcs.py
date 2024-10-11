
import aiohttp

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
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None