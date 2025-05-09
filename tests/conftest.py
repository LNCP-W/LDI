import asyncio
from datetime import date
from typing import AsyncGenerator

import pytest
from base import Base
from db import DB
from dependencies import get_db as gdb
from main import app
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

# Use an in-memory SQLite database for fast and isolated testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async-compatible SQLAlchemy engine and session factory
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function", autouse=True)
def prepare_test_database():
    """
    Fixture that automatically prepares the database before each test
    and tears it down afterward. This ensures test isolation.

    Scope: function — runs for each test function.
    Autouse: True — automatically applied to all tests.
    """
    asyncio.run(_setup_db())
    yield
    asyncio.run(_teardown_db())


async def _setup_db():
    """
    Asynchronously creates all tables in the test database
    using metadata from the Base declarative class.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _teardown_db():
    """
    Asynchronously drops all tables in the test database
    after the test is complete to ensure clean state.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def get_db() -> AsyncGenerator[DB, None]:
    """
    Provides an asynchronous database session (wrapped in DB abstraction)
    for use within a test.

    Usage:
        async def test_example(get_db):
            ...

    Scope: function — a new DB instance is provided for each test.
    """
    async with TestingSessionLocal() as session:
        yield DB(session)


@pytest.fixture
def override_dependencies():

    class FakeDB:
        async def get_weather(self, city: str, day: date):
            return [
                {
                    "id": 1,
                    "city": city,
                    "time_point": f"{day}T14:00:00",
                    "temperature": 21.5,
                }
            ]

    app.dependency_overrides.clear()
    app.dependency_overrides[gdb] = FakeDB
    yield app
    app.dependency_overrides.clear()
