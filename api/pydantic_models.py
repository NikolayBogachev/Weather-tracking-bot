from datetime import datetime

from pydantic import BaseModel


class TunedModel(BaseModel):
    """
    Базовый класс для всех моделей.
    Конфигурация:
    - from_attributes: позволяет создавать модели из словарей атрибутов.
    """

    class Config:
        from_attributes = True


class WeatherRequestLogBase(TunedModel):
    user_id: int
    command: str
    response: str
    created_at: datetime


class WeatherRequestLogResponse(WeatherRequestLogBase):
    id: int  # Добавляем поле id для ответа