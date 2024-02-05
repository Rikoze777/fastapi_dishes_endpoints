import json

from fastapi import Depends
from pydantic import UUID4

from app.database.db import get_redis
from app.repository.menu_repo import MenuRepositary
from app.schemas import schemas


class MenuService:
    def __init__(self, repository: MenuRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_menu(self, id: UUID4) -> schemas.Menu:
        menu_id = str(id)
        menu = self.repository.get_menu(id)
        if not self.cache.get(menu_id):
            menu = self.repository.get_menu(id)
            self.cache.set(menu_id, json.dumps(menu))
            self.cache.expire(menu_id, 300)
        return menu

    def get_menu_list(self) -> list:
        list_menu = self.repository.get_menu_list()
        if not self.cache.get('menu'):
            self.cache.set('menu', json.dumps(list_menu))
            self.cache.expire('menu', 300)
        return list_menu

    def create_menu(self, menu: schemas.MenuCreate) -> schemas.MenuCreate:
        result = self.repository.create_menu(menu)
        self.cache.delete('menu')
        return self.repository.get_menu(result.id)

    def update_menu(self,
                    id: UUID4,
                    menu: schemas.MenuUpdate) -> schemas.MenuUpdate:
        menu_id = str(id)
        self.repository.update_menu(id, menu)
        self.cache.delete(menu_id)
        self.cache.delete('menu')
        return self.repository.get_menu(id)

    def delete_menu(self, id: UUID4):
        menu_id = str(id)
        self.repository.delete_menu(id)
        self.cache.delete(menu_id)
        self.cache.delete('menu', 'submenu', 'dishes')

    def get_complex_query(self, menu_id: UUID4) -> dict:
        query = self.repository.get_complex_query(menu_id)
        menu, submenu_count, dishes_count = query
        menu_dict = {
            'id': id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenu_count,
            'dishes_count': dishes_count,
        }
        return menu_dict
