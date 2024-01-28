from app.tests.conftest import client
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID


TEST_SUBMENU_ID = "9ee49a1f-1ea9-4ca1-a0c9-6f20bf31196c"
SUBMENU_CREATE_DATA = {"title": "Test submenu",
                       "description": "Test description submenu"}
SUBMENU_UPDATE_DATA = {"title": "Test update submenu",
                       "description": "Test update description submenu"}


def test_get_empty_submenu(delete_menus):
    response = client.get(f"/api/v1/menus/{TEST_MENU_ID}/submenus")
    assert response.status_code == 200
    assert response.json() == []


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


def test_get_menu_list(menu_id):
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{menu_id}",
            "title": "Test menu",
            "description": "Test description menu",
            "submenus_count": 0,
            "dishes_count": 0
        }
    ]


def test_add_submenu(menu_id):
    data = SUBMENU_CREATE_DATA
    response = client.post(f"/api/v1/menus/{menu_id}/submenus",
                           json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "dishes_count" in menu


def test_get_submenu_list(menu_id, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{submenu_id}",
            "title": "Test submenu",
            "description": "Test description submenu",
            "dishes_count": 0
        }
    ]


def test_get_submenu(menu_id, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert response.status_code == 200
    menu = response.json()
    assert "dishes_count" in menu


def test_update_submenu(menu_id, submenu_id):
    data = SUBMENU_UPDATE_DATA
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/",
                            json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "dishes_count" in menu


def test_get_updated_submenu(menu_id, submenu_id):
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/")
    assert response.status_code == 200
    menu = response.json()
    assert "dishes_count" in menu


def test_get_submenu_not_exists(delete_menus):
    response = client.get(f"/api/v1/menus/{TEST_MENU_ID}/submenus/{TEST_SUBMENU_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}
