from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import UUID4
import pytest

from app.routers import dishes_router, menu_router, submenu_router
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.test_submenu import SUBMENU_CREATE_DATA, TEST_SUBMENU_ID
from app.tests.utils import reverse

TEST_DISH_ID = "c5d1e8e5-dcd0-4887-a9dd-7147ca4190e0"
DISH_CREATE_DATA = {
    "title": "Test dish",
    "description": "Test description dish",
    "price": "16.111",
}
DISH_UPATE_DATA = {
    "title": "Test update dish",
    "description": "Test update description dish",
    "price": "16.2111",
}


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_add_submenu(client: AsyncClient, menu_id: UUID4) -> None:
    data = SUBMENU_CREATE_DATA
    response = await client.post(
        reverse(submenu_router.add_submenu, menu_id=menu_id), json=data
    )
    assert response.status_code == 201
    menu = response.json()
    assert menu["title"] == data["title"]
    assert menu["description"] == data["description"]
    assert "id" in menu
    assert "dishes_count" in menu


@pytest.mark.asyncio
async def test_add_dish(client: AsyncClient, menu_id: UUID4, submenu_id: UUID4) -> None:
    data = DISH_CREATE_DATA
    response = await client.post(
        reverse(dishes_router.add_dish, menu_id=menu_id, submenu_id=submenu_id),
        json=data,
    )
    assert response.status_code == 201
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "id" in dish
    assert "price" in dish
    assert dish["price"] == str(round(float(data["price"]), 2))


@pytest.mark.asyncio
async def test_get_dish_list(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    response = await client.get(
        reverse(dishes_router.get_dishes_list, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": dish_id,
            "title": "Test dish",
            "description": "Test description dish",
            "price": "16.11",
        }
    ]


@pytest.mark.asyncio
async def test_get_dish(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    response = await client.get(
        reverse(
            dishes_router.get_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
    )
    assert response.status_code == 200
    dish = response.json()
    assert "price" in dish


@pytest.mark.asyncio
async def test_update_dish(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    data = DISH_UPATE_DATA
    response = await client.patch(
        reverse(
            dishes_router.update_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        ),
        json=data,
    )
    assert response.status_code == 200
    dish = response.json()
    assert dish["title"] == data["title"]
    assert dish["description"] == data["description"]
    assert "price" in dish
    assert dish["price"] == str(round(float(data["price"]), 2))


@pytest.mark.asyncio
async def test_get_update_dish(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    response = await client.get(
        reverse(
            dishes_router.get_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
    )
    assert response.status_code == 200
    dish = response.json()
    assert "price" in dish


@pytest.mark.asyncio
async def test_delete_dish(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    response = await client.delete(
        reverse(
            dishes_router.delete_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
    )
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "The dish has been deleted"}


@pytest.mark.asyncio
async def test_get_empty_dish(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.get(
        reverse(dishes_router.get_dishes_list, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_dish_after_delete(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.get(
        reverse(
            dishes_router.get_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=TEST_DISH_ID,
        )
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


@pytest.mark.asyncio
async def test_delete_submenu(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.delete(
        reverse(submenu_router.delete_submenu, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "Submenu has been deleted"}


@pytest.mark.asyncio
async def test_get_submenu_after_delete(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.get(
        reverse(submenu_router.get_submenu, menu_id=menu_id, submenu_id=TEST_SUBMENU_ID)
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "submenu not found"}


@pytest.mark.asyncio
async def test_delete_menu(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.delete(reverse(menu_router.delete_menu, id=menu_id))
    assert response.status_code == 200
    assert response.json() == {"status": "true", "message": "Menu has been deleted"}


@pytest.mark.asyncio
async def test_get_menu_after_delete(client: AsyncClient) -> None:
    response = await client.get(reverse(menu_router.get_menu, id=TEST_MENU_ID))
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}
