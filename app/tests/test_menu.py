from fastapi.testclient import TestClient
from pydantic import UUID4

from app.routers import menu_router
from app.tests.utils import reverse

TEST_MENU_ID = 'c36c1308-8f73-41df-8a11-6bb2f753ffb7'
MENU_CREATE_DATA = {'title': 'Test menu',
                    'description': 'Test description menu'}
MENU_UPDATE_DATA = {'title': 'Test update menu',
                    'description': 'Test update description menu'}


def test_get_empty_menu(test_client: TestClient,
                        delete_menus: None) -> None:
    response = test_client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == []


def test_add_menu(test_client: TestClient,
                  delete_menus: None) -> None:
    data = MENU_CREATE_DATA
    response = test_client.post(reverse(menu_router.add_menu), json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'id' in menu
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


def test_get_menu_list(test_client: TestClient,
                       menu_id: UUID4) -> None:
    response = test_client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': f'{menu_id}',
            'title': 'Test menu',
            'description': 'Test description menu',
            'submenus_count': 0,
            'dishes_count': 0
        }
    ]


def test_get_menu(test_client: TestClient,
                  menu_id: UUID4) -> None:
    response = test_client.get(reverse(menu_router.get_menu, id=menu_id))
    assert response.status_code == 200
    menu = response.json()
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


def test_update_menu(test_client: TestClient,
                     menu_id: UUID4) -> None:
    data = MENU_UPDATE_DATA
    response = test_client.patch(reverse(menu_router.update_menu, id=menu_id),
                                 json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


def test_get_update_menu_list(test_client: TestClient,
                              menu_id: UUID4) -> None:
    response = test_client.get(reverse(menu_router.get_menu_list))
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': f'{menu_id}',
            'title': 'Test update menu',
            'description': 'Test update description menu',
            'submenus_count': 0,
            'dishes_count': 0
        }
    ]


def test_delete_menu(test_client: TestClient,
                     menu_id: UUID4) -> None:
    response = test_client.delete(reverse(menu_router.delete_menu, id=menu_id))
    assert response.status_code == 200
    assert response.json() == {'status': 'true',
                               'message': 'Menu has been deleted'}


def test_get_menu_not_exists(test_client: TestClient,
                             delete_menus: None) -> None:
    response = test_client.get(reverse(menu_router.get_menu, id=TEST_MENU_ID))
    assert response.status_code == 404
    assert response.json() == {'detail': 'menu not found'}
