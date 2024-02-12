import pytest
from httpx import AsyncClient
from pydantic import UUID4

from app.routers import menu_router, submenu_router
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.utils import reverse

TEST_SUBMENU_ID = '9ee49a1f-1ea9-4ca1-a0c9-6f20bf31196c'
SUBMENU_CREATE_DATA = {
    'title': 'Test submenu',
    'description': 'Test description submenu',
}
SUBMENU_UPDATE_DATA = {
    'title': 'Test update submenu',
    'description': 'Test update description submenu',
}


@pytest.mark.asyncio
async def test_get_empty_submenu(client: AsyncClient, delete_menus: None) -> None:
    response = await client.get(
        reverse(submenu_router.get_submenu_list, menu_id=TEST_MENU_ID)
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_add_menu(
    client: AsyncClient, menu_id: UUID4, delete_menus: None
) -> None:
    data = MENU_CREATE_DATA
    response = await client.post(reverse(menu_router.add_menu), json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'id' in menu
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_get_menu_list(client: AsyncClient, menu_id: UUID4) -> None:
    response = await client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': f'{menu_id}',
            'title': 'Test menu',
            'description': 'Test description menu',
        }
    ]


@pytest.mark.asyncio
async def test_add_submenu(client: AsyncClient, menu_id: UUID4) -> None:
    data = SUBMENU_CREATE_DATA
    response = await client.post(
        reverse(submenu_router.add_submenu, menu_id=menu_id), json=data
    )
    assert response.status_code == 201
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'id' in menu
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_get_submenu_list(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.get(
        reverse(submenu_router.get_submenu_list, menu_id=menu_id)
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': f'{submenu_id}',
            'title': 'Test submenu',
            'description': 'Test description submenu',
            'dishes_count': 0,
        }
    ]


@pytest.mark.asyncio
async def test_get_submenu(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.get(
        reverse(submenu_router.get_submenu, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    menu = response.json()
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_update_submenu(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    data = SUBMENU_UPDATE_DATA
    response = await client.patch(
        reverse(submenu_router.update_submenu, menu_id=menu_id, submenu_id=submenu_id),
        json=data,
    )
    assert response.status_code == 200
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_get_updated_submenu(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    response = await client.get(
        reverse(submenu_router.get_submenu, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    menu = response.json()
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_get_submenu_not_exists(client: AsyncClient, delete_menus: None) -> None:
    response = await client.get(
        reverse(
            submenu_router.get_submenu, menu_id=TEST_MENU_ID, submenu_id=TEST_SUBMENU_ID
        )
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
