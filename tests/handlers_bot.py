
from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from TG.bot import bot
from funcs import fetch_weather_with_cache
from initdb import async_session
from database.models import log_request, get_user_city, save_user_city

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):

    await message.reply("Привет! Я бот, который сообщает погоду."
                        " Введи команду /weather город для получения информации.")


@router.message(Command("weather"))
async def get_weather(message: Message, bot: Bot, redis):
    """
    Обработчик команды /weather для получения прогноза погоды.
    Аргументом команды является название города, если не указан, то используется
    сохранённый город пользователя.
    """

    command_parts = message.text.split(maxsplit=1)

    async with async_session() as session:

        saved_city = await get_user_city(session, message.from_user.id)

    if len(command_parts) > 1:
        city_name = command_parts[1]

        if not city_name.isalpha():
            await message.reply("Название города должно содержать только буквы.")
            return
    else:

        if saved_city:
            city_name = saved_city
            await message.reply(f"Использую сохранённый город: {city_name}")
        else:

            await message.reply("Пожалуйста, укажи название города после команды или сохраните его в настройках."
                                " Пример: /weather Москва")
            return

    await message.reply(f"Ищу погоду для города: {city_name}...")
    weather_data = await fetch_weather_with_cache(city_name, bot, message, redis)

    if weather_data:
        """
        Если данные о погоде успешно получены, формируем ответное сообщение с подробностями
        (температура, описание, влажность, скорость ветра).
        """
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        weather_message = (
            f"Погода в городе {city_name}:\n"
            f"Температура: {temp}°C (Ощущается как {feels_like}°C)\n"
            f"Описание: {description}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )

        await message.reply(weather_message)

        async with async_session() as session:
            """
            Логирование запроса погоды в базу данных, а также обновление сохранённого города
            для пользователя, если он запросил новый город.
            """
            # Логирование запроса
            await log_request(session, message.from_user.id, message.text, weather_message)

            if saved_city != city_name:
                await save_user_city(session, message.from_user.id, city_name)
    else:

        await message.reply(f"Город {city_name} не найден. Проверьте правильность написания.")
