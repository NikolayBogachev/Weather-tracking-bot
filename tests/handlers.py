import sys
from datetime import datetime
from typing import List, Optional

from loguru import logger
from sqlalchemy import select

from api.pydantic_models import WeatherRequestLogResponse
from initdb import AsyncSession, get_db
from fastapi import APIRouter, Query, Depends, HTTPException

from database.models import WeatherRequest

logger.remove()  # Удалите все существующие обработчики
logger.add(sys.stdout, level="INFO", format="{time} {level} {message}", backtrace=True, diagnose=True)


router = APIRouter()


@router.get("/logs", response_model=List[WeatherRequestLogResponse])
async def get_logs(
        limit: int = Query(10, description="Количество записей на странице"),
        offset: int = Query(0, description="Смещение от начала"),
        start_date: Optional[datetime] = Query(None, description="Начальная дата для фильтрации"),
        end_date: Optional[datetime] = Query(None, description="Конечная дата для фильтрации"),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение логов запросов погоды.

    Аргументы:
    - `limit` (int): Количество записей для вывода на странице, по умолчанию 10.
    - `offset` (int): Смещение от начала, для пагинации, по умолчанию 0.
    - `start_date` (Optional[datetime]): Фильтрация по начальной дате (необязательно).
    - `end_date` (Optional[datetime]): Фильтрация по конечной дате (необязательно).
    - `db` (AsyncSession): Сессия базы данных, предоставляется через `Depends(get_db)`.

    Логи:
    - Выполняется запрос к базе данных на получение логов с фильтрацией по дате и пагинацией.
    - В случае успеха выводится информация о количестве полученных логов.
    - В случае ошибки выбрасывается HTTPException с кодом 500.

    Возвращает:
    - Список логов запросов погоды в формате `WeatherRequestLogResponse`.
    """

    # Создание запроса для получения логов
    query = select(WeatherRequest)

    # Фильтрация по времени
    if start_date:
        query = query.where(WeatherRequest.created_at >= start_date)
    if end_date:
        query = query.where(WeatherRequest.created_at <= end_date)

    # Пагинация
    query = query.limit(limit).offset(offset)

    try:
        result = await db.execute(query)
        logs = result.scalars().all()
        logger.info(f"Fetched {len(logs)} logs.")
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при запросе логов")

    return logs


@router.get("/logs/{user_id}", response_model=List[WeatherRequestLogResponse])
async def get_logs_by_user(
        user_id: int,
        limit: int = Query(10, description="Количество записей на странице"),
        offset: int = Query(0, description="Смещение от начала"),
        start_date: Optional[datetime] = Query(None, description="Начальная дата для фильтрации"),
        end_date: Optional[datetime] = Query(None, description="Конечная дата для фильтрации"),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение логов запросов погоды для конкретного пользователя по его `user_id`.

    Аргументы:
    - `user_id` (int): ID пользователя, чьи логи нужно получить.
    - `limit` (int): Количество записей для вывода на странице, по умолчанию 10.
    - `offset` (int): Смещение от начала, для пагинации, по умолчанию 0.
    - `start_date` (Optional[datetime]): Фильтрация по начальной дате (необязательно).
    - `end_date` (Optional[datetime]): Фильтрация по конечной дате (необязательно).
    - `db` (AsyncSession): Сессия базы данных, предоставляется через `Depends(get_db)`.

    Логи:
    - Выполняется запрос к базе данных для получения логов по `user_id`, с фильтрацией по дате и пагинацией.
    - В случае успеха выводится информация о количестве полученных логов для конкретного пользователя.
    - В случае ошибки выбрасывается HTTPException с кодом 500.

    Возвращает:
    - Список логов запросов погоды для пользователя в формате `WeatherRequestLogResponse`.
    """

    # Создание запроса для получения логов по user_id
    query = select(WeatherRequest).where(WeatherRequest.user_id == user_id)

    # Фильтрация по времени
    if start_date:
        query = query.where(WeatherRequest.created_at >= start_date)
    if end_date:
        query = query.where(WeatherRequest.created_at <= end_date)

    # Пагинация
    query = query.limit(limit).offset(offset)

    try:
        result = await db.execute(query)
        logs = result.scalars().all()
        logger.info(f"Fetched {len(logs)} logs for user_id={user_id}.")
    except Exception as e:
        logger.error(f"Error fetching logs for user_id={user_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при запросе логов пользователя")

    return logs
