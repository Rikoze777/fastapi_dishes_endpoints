import json
from typing import List
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
        return submenu

    def get_submenu_list(self,
                         menu_id: UUID4) -> List[schemas.Submenu]:
        submenus = self.repository.get_submenu_list(menu_id)
        return submenus

    def create_submenu(self,
                       menu_id: UUID4,
                       submenu: schemas.SubmenuCreate) -> schemas.Submenu:
        result = self.repository.create_submenu(menu_id, submenu)
        return self.repository.get_submenu(menu_id, result.id)

    def update_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4,
                       submenu: schemas.SubmenuUpdate) -> schemas.Submenu:
        result = self.repository.update_submenu(menu_id, submenu_id, submenu)
        return self.repository.get_submenu(menu_id, result.id)

    def delete_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4):
        self.repository.delete_submenu(menu_id, submenu_id)
