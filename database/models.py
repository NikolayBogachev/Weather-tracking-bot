from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    TIMESTAMP, BigInteger, select, func
)
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class WeatherRequest(Base):
    __tablename__ = "weather_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    command = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    response = Column(String, nullable=False)

    # Связь с UserSettings
    settings = relationship("UserSettings", back_populates="user", uselist=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('weather_requests.user_id'), unique=True, nullable=False)
    city = Column(String, nullable=True)

    # Связь с WeatherRequest
    user = relationship("WeatherRequest", back_populates="settings")


async def log_request(db_session: AsyncSession, user_id: int, command: str, response: str):
    new_log = WeatherRequest(user_id=user_id, command=command, response=response)
    db_session.add(new_log)
    await db_session.commit()


# Получение сохранённого города пользователя
async def get_user_city(db: AsyncSession, user_id: int) -> Optional[str]:
    result = await db.execute(select(UserSettings).where(user_id == UserSettings.user_id))
    settings = result.scalars().first()
    return settings.city if settings else None


# Сохранение нового города для пользователя
async def save_user_city(db: AsyncSession, user_id: int, city_name: str):
    result = await db.execute(select(UserSettings).where(user_id == UserSettings.user_id))
    settings = result.scalars().first()

    if settings:
        settings.city = city_name
    else:
        new_settings = UserSettings(user_id=user_id, city=city_name)
        db.add(new_settings)

    await db.commit()