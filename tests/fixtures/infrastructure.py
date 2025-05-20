from app.settings import Settings
from app.infrastructure.database.database import Base
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@pytest_asyncio.fixture
def settings():
    return Settings()

test_engine = create_async_engine(url="postgresql+asyncpg://postgres:password@0.0.0.0:5432/pomodoro-test", future=True, echo=True, pool_pre_ping=True)
test_async_session_maker = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session", autouse=True)
async def async_db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def get_db_session() -> AsyncSession:
    return AsyncSession()


@pytest_asyncio.fixture()
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
                await session.commit()