import json
from typing import List
from fastapi import Depends
from pydantic import UUID4
from app.crud.menu_crud import MenuRepositary
from app.database.db import get_redis
from app.schemas import schemas


class MenuService:
    def __init__(self, repository: MenuRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_menu(self, id: UUID4) -> schemas.Menu:
        menu_id = str(id)
        if not self.cache.get(menu_id):
            menu = self.repository.get_menu(id)
            self.cache.set(menu_id, json.dumps(menu))
            self.cache.expire(menu_id, 300)
            return menu
        else:
            return json.loads(self.cache.get(menu_id))

    def get_menu_list(self) -> List[schemas.Menu]:
        if not self.cache.get('menu'):
            list_menu = self.repository.get_menu_list()
            self.cache.set('menu', json.dumps(list_menu))
            self.cache.expire('menu', 300)
            return list_menu
        else:
            return json.loads(self.cache.get('menu'))

    def create_menu(self, menu: schemas.MenuCreate) -> schemas.MenuCreate:
        result = self.repository.create_menu(menu)
        self.cache.delete('menu')
        return result

    def update_menu(self,
                    id: UUID4,
                    menu: schemas.MenuUpdate) -> schemas.MenuUpdate:
        menu_id = str(id)
        self.repository.update_menu(id, menu)
        self.cache.delete(menu_id)
        self.cache.delete('menu')
        return self.repository.get_menu(menu_id)

    def delete_menu(self, id: UUID4):
        menu_id = str(id)
        self.repository.delete_menu(id)
        self.cache.delete(menu_id)
        self.cache.delete('menu')

    def get_complex_query(self, menu_id: UUID4) -> schemas.Menu:
        return self.repository.get_complex_query(menu_id)
