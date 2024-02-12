import pytest
from httpx import AsyncClient
from pydantic import UUID4

from app.routers import dishes_router, menu_router, submenu_router
from app.tests.test_dish import TEST_DISH_ID
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.test_submenu import SUBMENU_CREATE_DATA, TEST_SUBMENU_ID
from app.tests.utils import reverse

DISH_CREATE_DATA = {
    'title': 'Test dish 1',
    'description': 'Test description dish 1',
    'price': '16.222',
}
DISH_CREATE_DATA_SECOND = {
    'title': 'Test dish 2',
    'description': 'Test description dish 2',
    'price': '16.333',
}


@pytest.mark.asyncio
async def test_add_menu(client: AsyncClient, delete_menus: None) -> None:
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
async def test_add_dish_first(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    data = DISH_CREATE_DATA
    response = await client.post(
        reverse(dishes_router.add_dish, menu_id=menu_id, submenu_id=submenu_id),
        json=data,
    )
    assert response.status_code == 201
    dish = response.json()
    assert dish['title'] == data['title']
    assert dish['description'] == data['description']
    assert 'id' in dish
    assert 'price' in dish
    assert dish['price'] == str(round(float(data['price']), 2))


@pytest.mark.asyncio
async def test_all_data(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4
) -> None:
    menu = MENU_CREATE_DATA
    dish = DISH_CREATE_DATA
    submenu = SUBMENU_CREATE_DATA
    response = await client.get(reverse(menu_router.get_all_menus))
    assert response.status_code == 200
    m_id = menu_id
    s_id = submenu_id
    d_id = dish_id
    response_data = response.json()
    assert response_data == [
        {
            'id': m_id,
            'title': menu['title'],
            'description': menu['description'],
            'submenus': [
                {
                    'id': s_id,
                    'title': submenu['title'],
                    'description': submenu['description'],
                    'menu_id': m_id,
                    'dishes': [
                        {
                            'id': d_id,
                            'title': dish['title'],
                            'description': dish['description'],
                            'price': 16.22,
                            'submenu_id': s_id,
                        },
                    ],
                }
            ],
        }
    ]


@pytest.mark.asyncio
async def test_add_dish_second(
    client: AsyncClient, menu_id: UUID4, submenu_id: UUID4
) -> None:
    data = DISH_CREATE_DATA_SECOND
    response = await client.post(
        reverse(dishes_router.add_dish, menu_id=menu_id, submenu_id=submenu_id),
        json=data,
    )
    assert response.status_code == 201
    dish = response.json()
    assert dish['title'] == data['title']
    assert dish['description'] == data['description']
    assert 'id' in dish
    assert 'price' in dish
    assert dish['price'] == str(round(float(data['price']), 2))


@pytest.mark.asyncio
async def test_menu_complex_data(client: AsyncClient, menu_id: UUID4) -> None:
    menu = MENU_CREATE_DATA
    response = await client.get(reverse(menu_router.get_menu_counts, id=menu_id))
    assert response.status_code == 200
    result = response.json()
    assert 'id' in result
    assert result['title'] == menu['title']
    assert result['description'] == menu['description']
    assert 'submenus_count' in result
    assert 'dishes_count' in result


@pytest.mark.asyncio
async def test_delete_submenu(client, menu_id, submenu_id):
    response = await client.delete(
        reverse(submenu_router.delete_submenu, menu_id=menu_id, submenu_id=submenu_id)
    )
    assert response.status_code == 200
    assert response.json() == {'status': 'true', 'message': 'Submenu has been deleted'}


@pytest.mark.asyncio
async def test_get_dish_after_delete(client, menu_id):
    response = await client.get(
        reverse(
            dishes_router.get_dish,
            menu_id=menu_id,
            submenu_id=TEST_SUBMENU_ID,
            dish_id=TEST_DISH_ID,
        )
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'dish not found'}


@pytest.mark.asyncio
async def test_get_submenu(client, menu_id):
    response = await client.get(
        reverse(submenu_router.get_submenu, menu_id=menu_id, submenu_id=TEST_SUBMENU_ID)
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


@pytest.mark.asyncio
async def test_get_menu(client, menu_id):
    response = await client.get(reverse(menu_router.get_menu, id=menu_id))
    assert response.status_code == 200
    menu = response.json()
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


@pytest.mark.asyncio
async def test_delete_menu(client, menu_id):
    response = await client.delete(reverse(menu_router.delete_menu, id=menu_id))
    assert response.status_code == 200
    assert response.json() == {'status': 'true', 'message': 'Menu has been deleted'}


@pytest.mark.asyncio
async def test_get_menu_not_exists(client, delete_menus):
    response = await client.get(reverse(menu_router.get_menu, id=TEST_MENU_ID))
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
