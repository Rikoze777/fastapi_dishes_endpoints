from typing import AsyncGenerator, Generator
from httpx import AsyncClient
import pytest
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import Session, SessionTransaction
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database.models import Base
from app.main import app
from app.database.db import get_session
from app.config import Config


config = Config()
target_db = config.POSTGRES_DB_TEST
testbase_url = config.TESTBASE_URL
testbase_url_async = config.TESTBASE_URL_ASYNC

postgres_connection_url = config.POSTGRES_URL


@pytest.fixture(scope="session", autouse=True)
def test_database():
    engine = create_engine(postgres_connection_url, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{target_db}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{target_db}"'))
    engine.dispose()


@pytest.fixture
def db_engine():
    engine = create_engine(testbase_url)
    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield
        Base.metadata.drop_all(engine)

    engine.dispose()


@pytest.fixture
async def test_client() -> AsyncClient:
    async with AsyncClient(app=app) as c:
        yield c

@pytest.fixture
async def session() -> AsyncGenerator:
    async_engine = create_async_engine(testbase_url_async)
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()

    await async_engine.dispose()


@pytest.fixture()
async def delete_menus(test_client):
    response = await test_client.get("/api/v1/menus/")
    for menu in response.json():
        test_client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture()
async def menu_id(test_client):
    response = await test_client.get("api/v1/menus")
    for menu in response.json():
        return menu['id']


@pytest.fixture()
async def submenu_id(test_client, menu_id):
    response = await test_client.get(f"/api/v1/menus/{menu_id}/submenus/")
    for submenu in response.json():
        return submenu['id']


@pytest.fixture()
async def dish_id(test_client, menu_id, submenu_id):
    response = await test_client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    for dish in response.json():
        return dish['id']
