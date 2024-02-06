import json
from typing import Any

from fastapi import Depends
from pydantic import UUID4

from app.database.db import get_redis
from app.repository.submenu_repo import SubmenuRepositary
from app.schemas import schemas


class SubmenuService:
    def __init__(self,
                 repository: SubmenuRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_submenu(self,
                    menu_id: UUID4,
                    submenu_id: UUID4) -> dict[schemas.Submenu, Any]:
        """
        Get a submenu from the repository by menu_id and submenu_id.

        Args:
            menu_id (UUID4): The ID of the menu.
            submenu_id (UUID4): The ID of the submenu.

        Returns:
            schemas.Submenu: The retrieved submenu.
        """
        submenu = self.repository.get_submenu(menu_id, submenu_id)
        if not self.cache.get(str(submenu_id)):
            self.cache.set(str(submenu_id), json.dumps(submenu))
            self.cache.expire(str(submenu_id), 300)
            return submenu
        else:
            return json.loads(self.cache.get(str(submenu_id)))

    def get_submenu_list(self,
                         menu_id: UUID4) -> list[dict[schemas.Submenu, Any]]:
        """
        Get the list of submenus for a given menu ID.

        Args:
            menu_id (UUID4): The UUID of the menu for which to retrieve submenus.

        Returns:
            list: A list of submenus for the specified menu ID.
        """
        list_submenu = self.repository.get_submenu_list(menu_id)
        if not self.cache.get('submenu'):
            self.cache.set('submenu', json.dumps(list_submenu))
            self.cache.expire('submenu', 300)
            return list_submenu
        else:
            return json.loads(self.cache.get('submenu'))

    def create_submenu(self,
                       menu_id: UUID4,
                       submenu: schemas.SubmenuCreate) -> dict[schemas.Submenu, Any]:
        """
        Create a submenu for the given menu_id using the provided submenu information.

        Args:
            menu_id (UUID4): The ID of the menu for which the submenu is being created.
            submenu (schemas.SubmenuCreate): The information for the submenu being created.

        Returns:
            schemas.Submenu: The created submenu.
        """
        sub = self.repository.create_submenu(menu_id, submenu)
        self.cache.delete('menu', 'submenu')
        return self.repository.get_submenu(menu_id, sub.id)

    def update_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4,
                       submenu: schemas.SubmenuUpdate) -> dict[schemas.Submenu, Any]:
        """
        Update a submenu by menu_id and submenu_id with the given submenu data.

        Args:
            menu_id (UUID4): The UUID4 of the menu.
            submenu_id (UUID4): The UUID4 of the submenu.
            submenu (schemas.SubmenuUpdate): The data to update the submenu.

        Returns:
            schemas.Submenu: The updated submenu.
        """
        self.repository.update_submenu(menu_id,
                                       submenu_id,
                                       submenu)
        self.cache.delete(str(submenu_id))
        self.cache.delete('submenu')
        return self.repository.get_submenu(menu_id, submenu_id)

    def delete_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4) -> None:
        """
        Deletes a submenu from the menu.

        Args:
            menu_id (UUID4): The ID of the menu.
            submenu_id (UUID4): The ID of the submenu.

        Returns:
            None
        """
        self.repository.delete_submenu(menu_id, submenu_id)
        self.cache.delete(str(menu_id), str(submenu_id))
        self.cache.delete('menu', 'submenu', 'dishes')
