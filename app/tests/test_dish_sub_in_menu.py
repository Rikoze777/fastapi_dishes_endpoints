from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.test_submenu import SUBMENU_CREATE_DATA, TEST_SUBMENU_ID
from app.tests.test_dish import TEST_DISH_ID


DISH_CREATE_DATA = {"title": "Test dish 1",
                    "description": "Test description dish 1",
                    "price": "16.222"}
DISH_CREATE_DATA_SECOND = {"title": "Test dish 2",
                           "description": "Test description dish 2",
                           "price": "16.333"}


def test_add_menu(test_client, delete_menus):
    data = MENU_CREATE_DATA
    response = test_client.post("/api/v1/menus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_add_submenu(test_client, menu_id):
    data = SUBMENU_CREATE_DATA
    response = test_client.post(f"/api/v1/menus/{menu_id}/submenus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "dishes_count" in menu


def test_add_dish_first(test_client, menu_id, submenu_id):
    data = DISH_CREATE_DATA
    response = test_client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=data)
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_add_dish_second(test_client, menu_id, submenu_id):
    data = DISH_CREATE_DATA_SECOND
    response = test_client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=data)
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish['price'] == str(round(float(data['price']), 2))


def test_menu_complex_data(test_client, menu_id):
    menu = MENU_CREATE_DATA
    response = test_client.get(f"/api/v1/menus/{menu_id}/count")
    assert response.status_code == 200
    result = response.json()
    assert "id" in result
    assert result["title"] == menu["title"]
    assert result["description"] == menu["description"]
    assert "submenus_count" in result
    assert "dishes_count" in result


def test_delete_submenu(test_client, menu_id, submenu_id):
    response = test_client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true",
                               "message": "Submenu has been deleted"}


def test_get_dish_after_delete(test_client, menu_id):
    response = test_client.get(f"/api/v1/menus/{menu_id}/submenus/{TEST_SUBMENU_ID}/dishes/{TEST_DISH_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_get_submenu(test_client, menu_id):
    response = test_client.get(f"/api/v1/menus/{menu_id}/submenus/{TEST_SUBMENU_ID}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


def test_get_menu(test_client, menu_id):
    response = test_client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    menu = response.json()
    assert "submenus_count" in menu
    assert "dishes_count" in menu


def test_delete_menu(test_client, menu_id):
    response = test_client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true",
                               "message": "Menu has been deleted"}


def test_get_menu_not_exists(test_client, delete_menus):
    response = test_client.get(f"/api/v1/menus/{TEST_MENU_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}