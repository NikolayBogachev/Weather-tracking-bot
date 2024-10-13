

import pytest_asyncio

from httpx import AsyncClient


from initdb import create_db_and_tables

from tests.main import app


@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_database():
    await create_db_and_tables()

    yield


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client