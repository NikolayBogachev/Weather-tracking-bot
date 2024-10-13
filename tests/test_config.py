import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from database.db import get_db # Импортируйте ваши модели и функции
from database.models import Base

# Настройка тестового движка
DATABASE_URL = "sqlite+aiosqlite:///./test_database.db"  # URL вашей тестовой базы данных


@pytest.fixture(scope="session")
def async_engine():
    # Создайте асинхронный движок базы данных
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    # Закройте движок после завершения всех тестов
    asyncio.run(engine.dispose())

@pytest.fixture(scope="function")
async def async_session(async_engine):
    # Создайте новую сессию для каждого теста
    async_session_factory = sessionmaker(
        bind=async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session_factory() as session:
        # Создайте таблицы в базе данных
        async with session.begin():
            await session.run_sync(Base.metadata.create_all)
        yield session
        # Удалите все данные после теста
        await session.run_sync(Base.metadata.drop_all)
