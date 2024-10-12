import asyncio
import sys


from TG.bot import dp, bot

from loguru import logger


from TG.handlers_bot import router
from config import config
from database.db import init_db


async def main() -> None:
    """
    Основная асинхронная функция для запуска бота.
    1. Инициализирует базу данных через init_db().
    2. Регистрирует все обработчики событий бота.
    3. Запускает polling для обработки сообщений и команд от пользователей.
    В случае завершения работы, закрывает сессию бота и выводит сообщение о завершении.
    """

    # Инициализация базы данных
    init_db()

    # Логируем сообщение о запуске бота
    logger.info("Бот запущен и готов к работе.")
    try:
        # Подключаем маршруты (handlers)
        dp.include_router(router)

        # Запуск Polling для отслеживания обновлений в Telegram
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота при завершении
        await bot.session.close()
        logger.info("Сессия бота закрыта.")

if __name__ == "__main__":
    """
    Блок для выполнения программы. Настраивает логирование, проверяет наличие
    переменной окружения BOT_TOKEN, инициализирует запуск основного цикла программы.

    Если токен не указан — выводит ошибку и завершает выполнение.
    Также обрабатываются прерывания (KeyboardInterrupt, SystemExit) и
    корректно завершается выполнение бота с логированием.
    """

    # Настраиваем логирование (вывод на консоль, уровень INFO)
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")

    # Проверка наличия BOT_TOKEN в конфигурации
    if not config.TOKEN:
        logger.error("BOT_TOKEN не указан. Пожалуйста, установите переменную окружения BOT_TOKEN.")
        sys.exit(1)

    try:
        # Запуск основного цикла с асинхронной функцией main()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Логируем завершение работы бота при прерывании
        logger.info("Бот остановлен.")