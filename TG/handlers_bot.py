
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from TG.funcs import fetch_weather

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.reply("Привет! Я бот, который сообщает погоду."
                        " Введи команду /weather <город> для получения информации.")


# Обработчик команды /weather <город>
@router.message(Command("weather"))
async def get_weather(message: Message):
    # Получаем аргументы после команды (город)
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) == 1:
        # Если город не указан
        await message.reply("Пожалуйста, укажи название города после команды. Пример: /weather Москва")
    else:
        city_name = command_parts[1]

        # Проверка: город должен быть текстом, длина должна быть больше 1 символа
        if not city_name.isalpha():
            await message.reply("Название города должно содержать только буквы.")
        else:
            await message.reply(f"Ищу погоду для города: {city_name}...")

            # Запрос погоды через API OpenWeatherMap
            weather_data = await fetch_weather(city_name)

            if weather_data:
                # Формируем ответ с данными о погоде
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
            else:
                await message.reply(f"Город {city_name} не найден. Проверьте правильность написания.")
