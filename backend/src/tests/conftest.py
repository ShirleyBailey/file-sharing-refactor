import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models import Base
import src.database as db_module
import src.service as service_module

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db(tmp_path, monkeypatch):
    """Create in-memory SQLite DB and patch the session maker for each test."""
    test_engine = create_async_engine(TEST_DB_URL)
    test_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "async_session_maker", test_session_maker)
    monkeypatch.setattr(service_module, "async_session_maker", test_session_maker)

    # Patch storage dir to tmp_path
    monkeypatch.setattr(service_module, "STORAGE_DIR", tmp_path)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def client():
    from src.app import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
