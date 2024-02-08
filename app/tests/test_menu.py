import pytest


TEST_MENU_ID = "c36c1308-8f73-41df-8a11-6bb2f753ffb7"
MENU_CREATE_DATA = {"title": "Test menu",
                    "description": "Test description menu"}
MENU_UPDATE_DATA = {"title": "Test update menu",
                    "description": "Test update description menu"}


@pytest.mark.anyio
async def test_get_empty_menu(test_client, delete_menus):
    response = await test_client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_add_menu(test_client, delete_menus):
    data = MENU_CREATE_DATA
    response = await test_client.post("/api/v1/menus", json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "submenus_count" in menu
    assert "dishes_count" in menu


@pytest.mark.anyio
async def test_get_menu_list(test_client, menu_id):
    response = test_client.get("/api/v1/menus")
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


@pytest.mark.anyio
async def test_get_menu(test_client, menu_id):
    response = await test_client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    menu = response.json()
    assert "submenus_count" in menu
    assert "dishes_count" in menu


@pytest.mark.anyio
async def test_update_menu(test_client, menu_id):
    data = MENU_UPDATE_DATA
    response = await test_client.patch(f"/api/v1/menus/{menu_id}/", json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "submenus_count" in menu
    assert "dishes_count" in menu


@pytest.mark.anyio
async def test_get_update_menu_list(test_client, menu_id):
    response = await test_client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{menu_id}",
            "title": "Test update menu",
            "description": "Test update description menu",
            "submenus_count": 0,
            "dishes_count": 0
        }
    ]


@pytest.mark.anyio
async def test_delete_menu(test_client, menu_id):
    response = await test_client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "true",
                               "message": "Menu has been deleted"}


@pytest.mark.anyio
async def test_get_menu_not_exists(test_client, delete_menus):
    response = await test_client.get(f"/api/v1/menus/{TEST_MENU_ID}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}