import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base
from app.main import app
from app.database.db import get_db
from app.config import Config


config = Config()

TESTBASE = config.TESTBASE_URL

engine = create_engine(TESTBASE)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture()
def delete_menus():
    response = client.get("/api/v1/menus/")
    for menu in response.json():
        client.delete(f"/api/v1/menus/{menu['id']}/")


@pytest.fixture()
def menu_id():
    response = client.get("api/v1/menus")
    for menu in response.json():
        return menu['id']


@pytest.fixture()
def submenu_id(menu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/")
    for submenu in response.json():
        return submenu['id']


@pytest.fixture()
def dish_id(menu_id, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
    for dish in response.json():
        return dish['id']
