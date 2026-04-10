import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models import Base
import src.database as db_module
import src.service as service_module
import src.tasks as tasks_module

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db(tmp_path, monkeypatch):
    test_engine = create_async_engine(TEST_DB_URL)
    test_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Patch session maker everywhere it's used
    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "async_session_maker", test_session_maker)
    monkeypatch.setattr(service_module, "async_session_maker", test_session_maker)
    monkeypatch.setattr(tasks_module, "async_session_maker", test_session_maker)

    # Patch storage dir in both service and tasks
    monkeypatch.setattr(service_module, "STORAGE_DIR", tmp_path)
    monkeypatch.setattr(tasks_module, "STORAGE_DIR", tmp_path)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def client():
    from src.app import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
