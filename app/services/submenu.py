import json

from fastapi import Depends
from pydantic import UUID4

from app.crud.submenu_crud import SubmenuRepositary
from app.database.db import get_redis
from app.schemas import schemas


class SubmenuService:
    def __init__(self,
                 repository: SubmenuRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_submenu(self,
                    menu_id: UUID4,
                    submenu_id: UUID4) -> schemas.Submenu:
        submenu = self.repository.get_submenu(menu_id, submenu_id)
        if not self.cache.get(str(submenu_id)):
            submenu = self.repository.get_submenu(menu_id, submenu_id)
            self.cache.set(str(submenu_id), json.dumps(submenu))
            self.cache.expire(str(submenu_id), 300)
            return submenu
        else:
            return json.loads(self.cache.get(submenu_id))

    def get_submenu_list(self,
                         menu_id: UUID4) -> list:
        if not self.cache.get('submenu'):
            list_submenu = self.repository.get_submenu_list(menu_id)
            self.cache.set('submenu', json.dumps(list_submenu))
            self.cache.expire('submenu', 300)
            return list_submenu
        else:
            return json.loads(self.cache.get('submenu'))

    def create_submenu(self,
                       menu_id: UUID4,
                       submenu: schemas.SubmenuCreate) -> schemas.Submenu:
        sub = self.repository.create_submenu(menu_id, submenu)
        self.cache.delete('menu', 'submenu')
        return sub

    def update_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4,
                       submenu: schemas.SubmenuUpdate) -> schemas.Submenu:
        update_submenu = self.repository.update_submenu(menu_id,
                                                        submenu_id,
                                                        submenu)
        self.cache.delete(str(submenu_id))
        self.cache.delete('submenu')
        return update_submenu

    def delete_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4):
        self.repository.delete_submenu(menu_id, submenu_id)
        self.cache.delete(str(menu_id), str(submenu_id))
        self.cache.delete('menu', 'submenu', 'dishes')
