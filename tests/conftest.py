import asyncio
import os
import sys
from typing import Any, Generator

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

# Получить путь к корневому каталогу проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Добавить корневой каталог в Python-путь
sys.path.append(project_root)

import settings
from db.session import get_db
from run import app

CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    print("open loop")
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    print("close loop")


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    print("run_migrations - start!")
    os.system("alembic init migrations")
    os.system("alembic revision --autogenerate -m 'run test migrations' ")
    os.system("alembic upgrade heads")
    print("run_migrations - stop!")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False,
                                 class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning}""")


async def _get_test_db():
    try:
        test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True,
                                          echo=True)
        test_async_session = sessionmaker(test_engine, expire_on_commit=False,
                                          class_=AsyncSession)
        yield test_async_session()
    except Exception as exception:
        print(f"{exception=}")
    finally:
        pass


@pytest_asyncio.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the 'db_session' fixture to override
    the 'get_db' dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM users WHERE user_id = $1;""",
                                          user_id)

    return get_user_from_database_by_uuid
