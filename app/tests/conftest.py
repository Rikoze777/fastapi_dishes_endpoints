from httpx import AsyncClient
import pytest
from typing import AsyncGenerator, AsyncIterator
from pydantic import UUID4
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.cache.redis import cache_instance
from app.config import Config
from app.database.db import Base, get_session
from app.main import app
from sqlalchemy.ext.asyncio import AsyncSession

config = Config()
target_db = config.POSTGRES_DB_TEST
testbase_url = config.TESTBASE_URL_ASYNC
postgres_connection_url = config.TESTBASE_URL

test_engine = create_async_engine(url=testbase_url, poolclass=NullPool, echo=True)
test_session_maker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
Base.metadata.bind = test_engine


async def override_scoped_session() -> AsyncIterator[async_sessionmaker]:
    yield test_session_maker


app.dependency_overrides[get_session] = override_scoped_session


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def prepare_cache():
    cache_instance.redis_client.flushall()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def delete_menus(client: AsyncClient) -> None:
    response = await client.get("/api/v1/menus/")
    for menu in response.json():
        await client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture
async def menu_id(client: AsyncClient) -> UUID4:
    response = await client.get("/api/v1/menus/")
    for menu in response.json():
        return menu["id"]


@pytest.fixture
async def submenu_id(client: AsyncClient, menu_id: UUID4) -> UUID4:
    response = await client.get(f"/api/v1/menus/{menu_id}/submenus")
    for submenu in response.json():
        return submenu["id"]


@pytest.fixture
async def dish_id(client: AsyncClient, menu_id: UUID4, submenu_id: UUID4) -> UUID4:
    dishes_url = f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes"
    response = await client.get(dishes_url)
    for dish in response.json():
        return dish["id"]
