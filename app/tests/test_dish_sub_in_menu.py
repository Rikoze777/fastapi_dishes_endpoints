from app.tests.conftest import client
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.test_submenu import SUBMENU_CREATE_DATA, TEST_SUBMENU_ID
from app.tests.test_dish import TEST_DISH_ID


DISH_CREATE_DATA = {"title": "Test dish 1",
                    "description": "Test description dish 1",
                    "price": "16.222"}
DISH_CREATE_DATA_SECOND = {"title": "Test dish 2",
                           "description": "Test description dish 2",
                           "price": "16.333"}


def test_add_menu(delete_menus):
    data = MENU_CREATE_DATA
    response = client.post("/api/v1/menus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_add_submenu(menu_id):
    data = SUBMENU_CREATE_DATA
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "dishes_count" in menu


def test_add_dish_first(menu_id, submenu_id):
    data = DISH_CREATE_DATA
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=data)
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_add_dish_second(menu_id, submenu_id):
    data = DISH_CREATE_DATA_SECOND
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=data)
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_delete_submenu(menu_id, submenu_id):
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true",
                               "message": "Submenu has been deleted"}


def test_get_dish_after_delete(menu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{TEST_SUBMENU_ID}/dishes/{TEST_DISH_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_get_submenu(menu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{TEST_SUBMENU_ID}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_get_menu(menu_id):
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    menu = response.json()
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_delete_menu(menu_id):
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true",
                               "message": "Menu has been deleted"}


def test_get_menu_not_exists(delete_menus):
    response = client.get(f"/api/v1/menus/{TEST_MENU_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}