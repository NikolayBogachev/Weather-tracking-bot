from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from database.models import Base

DATABASE_URL = "sqlite+aiosqlite:///./test.database"  # Используйте SQLite для простоты, замените на PostgreSQL в продакшене
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=True,
)
sync_engine = create_engine("sqlite:///./test.database")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise
    finally:
        await session.close()


def init_db():
    Base.metadata.create_all(bind=sync_engine)
