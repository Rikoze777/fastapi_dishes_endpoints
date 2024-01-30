import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.main import app
from app.database.db import get_db
from app.config import Config


config = Config()
target_db = config.POSTGRES_DB_TEST
testbase_url = config.TESTBASE_URL
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
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)()


@pytest.fixture
def test_client(db_session):
    def override_get_db():
        try:
            db = db_session
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def delete_menus(test_client):
    response = test_client.get("/api/v1/menus/")
    for menu in response.json():
        test_client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture()
def menu_id(test_client):
    response = test_client.get("api/v1/menus")
    for menu in response.json():
        return menu['id']


@pytest.fixture()
def submenu_id(test_client, menu_id):
    response = test_client.get(f"/api/v1/menus/{menu_id}/submenus/")
    for submenu in response.json():
        return submenu['id']


@pytest.fixture()
def dish_id(test_client, menu_id, submenu_id):
    response = test_client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    for dish in response.json():
        return dish['id']
