from tkinter import Menu
from typing import Annotated
from fastapi import BackgroundTasks, Depends
from app.database.db import get_async_session
from pydantic import UUID4
from app.repository.menu import MenuRepository
from app.cache.redis import cache_instance
from app.schemas.schemas import MenuCreate, MenuUpdate


class MenuService:

    def __init__(self, repository: MenuRepository = Depends()):
        self.repository = repository
        self.cache = cache_instance

    async def get_menu_list(self):
        return await self.cache("menu", self.repository.get_menu_list)

    async def get(self, menu_id: UUID4) -> Menu:
        return await self.cache.fetch(f"menu_{menu_id}",
                                      self.repository.get_menu,
                                      menu_id,)

    async def create(self,
                     menu_schema: MenuCreate,
                     background_tasks: BackgroundTasks,) -> Menu:
        menu = await self.repository.create_menu(menu_schema)
        background_tasks.add_task(self.cache.invalidate, "menu", "data")
        return menu

    async def update(self,
                     menu_id: UUID4,
                     menu_schema: MenuUpdate,
                     background_tasks: BackgroundTasks,) -> type[Menu]:
        item = await self.repository.update_menu(menu_id, menu_schema)
        background_tasks.add_task(
            self.cache.invalidate,
            "menu",
            f"menu_{menu_id}",
            "data",
        )
        return item

    async def delete(self,
                     menu_id: UUID4,
                     background_tasks: BackgroundTasks,) -> None:
        item = await self.repository.delete(menu_id)
        background_tasks.add_task(
            self.cache.invalidate,
            "menu",
            f"menu_{menu_id}",
            "data",
        )

    async def get_complex_query(self,
                                menu_id: UUID4,
                                background_tasks: BackgroundTasks,) -> Menu:
        result = self.repository.get_complex_query(menu_id)
        menu, submenu_count, dishes_count = result
        menu_dict = {
            "id": id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenu_count,
            "dishes_count": dishes_count,
        }
        background_tasks.add_task(
            self.cache.invalidate,
            "menu",
            f"menu_{menu_id}",
            "data",
        )
        return result
