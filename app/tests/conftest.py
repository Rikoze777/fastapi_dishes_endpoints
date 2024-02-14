import asyncio
from typing import AsyncGenerator, AsyncIterator

import pytest
from httpx import AsyncClient
from pydantic import UUID4
from sqlalchemy import NullPool, create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.cache.redis import cache_instance
from app.config import Config
from app.database.db import Base, get_session
from app.main import app

config = Config()
target_db = config.POSTGRES_DB_TEST
testbase_url = config.TESTBASE_URL_ASYNC
postgres_connection_url = config.TESTBASE_URL


def db_prep():
    print('dropping the old test db…')
    sync_engine = create_engine(postgres_connection_url)
    conn = sync_engine.connect()
    try:
        conn = conn.execution_options(autocommit=False)
        conn.execute(text('ROLLBACK'))
        conn.execute(text(f'DROP DATABASE {target_db}'))
    except ProgrammingError:
        print('Could not drop the database, probably does not exist.')
        conn.execute(text('ROLLBACK'))
    except OperationalError:
        print(
            "Could not drop database because it's being accessed by other users (psql prompt open?)"
        )
        conn.execute(text('ROLLBACK'))
    print(f'test db dropped! about to create {target_db}')
    conn.execute(text(f'CREATE DATABASE {target_db}'))
    try:
        conn.execute(
            text(
                f"create user {config.POSTGRES_USER} with encrypted password '{config.POSTGRES_PASSWORD}'"
            )
        )
    except Exception:
        print('User already exists.')
        conn.execute(
            text(
                f'grant all privileges on database {target_db} to {config.POSTGRES_USER}'
            )
        )
    conn.close()
    print('test db created')


test_engine = create_async_engine(url=testbase_url, poolclass=NullPool, echo=True)
Base.metadata.bind = test_engine

test_session_maker = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def override_scoped_session() -> AsyncIterator[async_sessionmaker]:
    yield test_session_maker


app.dependency_overrides[get_session] = override_scoped_session
Base.metadata.bind = test_engine


@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture
def prepare_cache():
    cache_instance.redis_client.flushall()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    db_prep()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
async def delete_menus(client: AsyncClient) -> None:
    response = await client.get('/api/v1/menus/')
    for menu in response.json():
        await client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture
async def menu_id(client: AsyncClient) -> UUID4:
    response = await client.get('/api/v1/menus/')
    for menu in response.json():
        return menu['id']


@pytest.fixture
async def submenu_id(client: AsyncClient, menu_id: UUID4) -> UUID4:
    response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    for submenu in response.json():
        return submenu['id']


@pytest.fixture
async def dish_id(client: AsyncClient, menu_id: UUID4, submenu_id: UUID4) -> UUID4:
    dishes_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
    response = await client.get(dishes_url)
    for dish in response.json():
        return dish['id']
