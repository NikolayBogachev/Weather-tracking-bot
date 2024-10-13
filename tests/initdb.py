
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import sessionmaker

from database.models import Base, WeatherRequest

DATABASE_URL = "sqlite+aiosqlite:///./test.databasedb"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine=engine, class_=AsyncSession, expire_on_commit=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise
    finally:
        await session.close()


async def create_db_and_tables():
    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_data_1():

    async with AsyncSession(engine) as session:
        async with session.begin():
            log = WeatherRequest(
                user_id=1, command='/weather Moscow', response='Погода в Москве...'
            )
            session.add(log)
            await session.commit()


async def create_data_2(user_id):

    async with AsyncSession(engine) as session:
        async with session.begin():

            test_log = WeatherRequest(user_id=user_id, command="test_command", response="test_response")
            session.add(test_log)
            await session.commit()


async def create_data_3(user_id):

    async with AsyncSession(engine) as session:
        async with session.begin():
            data_to_insert = [
                {
                    'command': 'test_command_1',
                    'created_at': datetime.strptime('2024-10-01', '%Y-%m-%d'),  # Convert to datetime
                    'response': 'test_response_1',
                    'user_id': user_id
                },
                {
                    'command': 'test_command_2',
                    'created_at': datetime.strptime('2024-10-02', '%Y-%m-%d'),  # Convert to datetime
                    'response': 'test_response_2',
                    'user_id': user_id
                }
            ]

            for data in data_to_insert:
                new_request = WeatherRequest(**data)
                session.add(new_request)

            await session.commit()
