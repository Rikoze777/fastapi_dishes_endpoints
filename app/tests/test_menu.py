from httpx import AsyncClient
from pydantic import UUID4
import pytest

from app.routers import menu_router
from app.tests.utils import reverse

TEST_MENU_ID = "c36c1308-8f73-41df-8a11-6bb2f753ffb7"
MENU_CREATE_DATA = {"title": "Test menu", "description": "Test description menu"}
MENU_UPDATE_DATA = {
    "title": "Test update menu",
    "description": "Test update description menu",
}


async def test_get_empty_menu(client: AsyncClient, delete_menus: None) -> None:
    response = await client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == []


async def test_add_menu(client: AsyncClient, delete_menus: None) -> None:
    data = MENU_CREATE_DATA
    response = await client.post(reverse(menu_router.add_menu), json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "submenus_count" in menu
    assert "dishes_count" in menu


async def test_get_menu_list(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{menu_id}",
            "title": "Test menu",
            "description": "Test description menu",
            "submenus_count": 0,
            "dishes_count": 0,
        }
    ]


async def test_get_menu(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.get(reverse(menu_router.get_menu, id=menu_id))
    assert response.status_code == 200
    menu = response.json()
    assert "submenus_count" in menu
    assert "dishes_count" in menu


async def test_update_menu(client: AsyncClient, menu_id: UUID4) -> None:
    data = MENU_UPDATE_DATA
    response = await client.patch(
        reverse(menu_router.update_menu, id=menu_id), json=data
    )
    assert response.status_code == 200
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "submenus_count" in menu
    assert "dishes_count" in menu


async def test_get_update_menu_list(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": f"{menu_id}",
            "title": "Test update menu",
            "description": "Test update description menu",
            "submenus_count": 0,
            "dishes_count": 0,
        }
    ]


async def test_delete_menu(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.delete(reverse(menu_router.delete_menu, id=menu_id))
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "Menu has been deleted"}


async def test_get_menu_not_exists(client: AsyncClient, delete_menus: None) -> None:
    response = await client.get(reverse(menu_router.get_menu, id=TEST_MENU_ID))
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
