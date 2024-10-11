import sys

from loguru import logger


from database.db import AsyncSession, get_db
from fastapi import APIRouter


logger.remove()  # Удалите все существующие обработчики
logger.add(sys.stdout, level="INFO", format="{time} {level} {message}", backtrace=True, diagnose=True)


router = APIRouter()

