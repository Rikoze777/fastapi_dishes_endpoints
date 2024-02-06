import json
from typing import Any

from fastapi import Depends
from pydantic import UUID4

from app.database.db import get_redis
from app.database.models import Menu
from app.repository.menu_repo import MenuRepositary
from app.schemas import schemas


class MenuService:
    def __init__(self, repository: MenuRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_menu(self, id: UUID4) -> dict[schemas.Menu, Any]:
        """
        Retrieves a menu from the repository by its ID and caches the result for 5 minutes if not already cached.

        Args:
            id: The UUID4 ID of the menu to retrieve.

        Returns:
            The retrieved menu as a schemas.Menu object.
        """
        menu_id = str(id)
        menu = self.repository.get_menu(id)
        if not self.cache.get(menu_id):
            menu = self.repository.get_menu(id)
            self.cache.set(menu_id, json.dumps(menu))
            self.cache.expire(menu_id, 300)
            return menu
        else:
            return json.loads(self.cache.get(menu_id))

    def get_menu_list(self) -> list:
        """
        Get the menu list from the repository and cache the result for 5 minutes if not already cached.

        :return: list
        """
        list_menu = self.repository.get_menu_list()
        if not self.cache.get('menu'):
            self.cache.set('menu', json.dumps(list_menu))
            self.cache.expire('menu', 300)
            return list_menu
        else:
            return json.loads(self.cache.get('menu'))

    def create_menu(self, menu: schemas.MenuCreate) -> dict[Menu, Any]:
        """
        Create a menu and return the created menu object.

        Args:
            menu (schemas.MenuCreate): The menu object to be created.

        Returns:
            schemas.MenuCreate: The created menu object.
        """
        result = self.repository.create_menu(menu)
        self.cache.delete('menu')
        return self.repository.get_menu(result.id)

    def update_menu(self,
                    id: UUID4,
                    menu: schemas.MenuUpdate) -> dict[Menu, Any]:
        """
        Update a menu in the repository and cache and return the updated menu.

        Args:
            id (UUID4): The ID of the menu to be updated.
            menu (MenuUpdate): The updated menu data.

        Returns:
            MenuUpdate: The updated menu data.
        """
        menu_id = str(id)
        self.repository.update_menu(id, menu)
        self.cache.delete(menu_id)
        self.cache.delete('menu')
        return self.repository.get_menu(id)

    def delete_menu(self, id: UUID4) -> None:
        """
        Delete a menu by its ID.

        Args:
            id (UUID4): The ID of the menu to be deleted.

        Returns:
            None
        """
        menu_id = str(id)
        self.repository.delete_menu(id)
        self.cache.delete(menu_id)
        self.cache.delete('menu', 'submenu', 'dishes')

    def get_complex_query(self, menu_id: UUID4) -> dict[str, Any]:
        """
        Get a complex query for a menu by its ID and return a dictionary with menu details, submenu count, and dishes count.

        :param menu_id: The ID of the menu (UUID4)
        :return: A dictionary containing the menu ID, title, description, submenu count, and dishes count
        :rtype: dict
        """
        query = self.repository.get_complex_query(menu_id)
        menu, submenu_count, dishes_count = query
        menu_dict = {
            'id': menu_id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenu_count,
            'dishes_count': dishes_count,
        }
        return menu_dict
