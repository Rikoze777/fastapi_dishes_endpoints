from app.routers import menu_router, submenu_router
from app.tests.test_menu import MENU_CREATE_DATA, TEST_MENU_ID
from app.tests.utils import reverse

TEST_SUBMENU_ID = '9ee49a1f-1ea9-4ca1-a0c9-6f20bf31196c'
SUBMENU_CREATE_DATA = {'title': 'Test submenu',
                       'description': 'Test description submenu'}
SUBMENU_UPDATE_DATA = {'title': 'Test update submenu',
                       'description': 'Test update description submenu'}


def test_get_empty_submenu(test_client, delete_menus):
    response = test_client.get(reverse(submenu_router.get_submenu_list))
    assert response.status_code == 200
    assert response.json() == []


def test_add_menu(test_client, menu_id, delete_menus):
    data = MENU_CREATE_DATA
    response = test_client.post(reverse(menu_router.add_menu), json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'id' in menu
    assert 'submenus_count' in menu
    assert 'dishes_count' in menu


def test_get_menu_list(test_client, menu_id):
    response = test_client.get(reverse(submenu_router.get_submenu_list))
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


def test_add_submenu(test_client, menu_id):
    data = SUBMENU_CREATE_DATA
    response = test_client.post(reverse(submenu_router.add_submenu,
                                        menu_id=menu_id),
                                json=data)
    assert response.status_code == 201
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'id' in menu
    assert 'dishes_count' in menu


def test_get_submenu_list(test_client, menu_id, submenu_id):
    response = test_client.get(reverse(submenu_router.get_submenu_list,
                                       menu_id=menu_id))
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': f'{submenu_id}',
            'title': 'Test submenu',
            'description': 'Test description submenu',
            'dishes_count': 0
        }
    ]


def test_get_submenu(test_client, menu_id, submenu_id):
    response = test_client.get(reverse(submenu_router.get_submenu,
                                       menu_id=menu_id,
                                       submenu_id=submenu_id))
    assert response.status_code == 200
    menu = response.json()
    assert 'dishes_count' in menu


def test_update_submenu(test_client, menu_id, submenu_id):
    data = SUBMENU_UPDATE_DATA
    response = test_client.patch(reverse(submenu_router.update_submenu,
                                         menu_id=menu_id,
                                         submenu_id=submenu_id),
                                 json=data)
    assert response.status_code == 200
    menu = response.json()
    assert menu['title'] == data['title']
    assert menu['description'] == data['description']
    assert 'dishes_count' in menu


def test_get_updated_submenu(test_client, menu_id, submenu_id):
    response = test_client.get(reverse(submenu_router.get_submenu,
                                       menu_id=menu_id,
                                       submenu_id=submenu_id))
    assert response.status_code == 200
    menu = response.json()
    assert 'dishes_count' in menu


def test_get_submenu_not_exists(test_client, delete_menus):
    response = test_client.get(reverse(submenu_router.get_submenu,
                                       menu_id=TEST_MENU_ID,
                                       submenu_id=TEST_SUBMENU_ID))
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}
