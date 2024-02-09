from fastapi import BackgroundTasks, Depends
from pydantic import UUID4

from app.cache.redis import cache_instance
from app.repository.exceptions import MenuExistsException
from app.repository.menu_repo import MenuRepository
from app.schemas.schemas import Menu, MenuCreate, MenuExtended, MenuUpdate


class MenuService:

    def __init__(self, repository: MenuRepository = Depends()):
        self.repository = repository
        self.cache = cache_instance

    async def get_menu_list(self):
        return await self.cache.fetch("menu", self.repository.get_menu_list)

    async def get(self, menu_id: UUID4) -> Menu:
        return await self.cache.fetch(
            f"menu_{menu_id}",
            self.repository.get_menu,
            menu_id,
        )

    async def create(
        self,
        menu_schema: MenuCreate,
        background_tasks: BackgroundTasks,
    ) -> Menu:
        menu = await self.repository.create_menu(menu_schema)
        background_tasks.add_task(self.cache.invalidate, "menu")
        return menu

    async def update(
        self,
        menu_id: UUID4,
        menu_schema: MenuUpdate,
        background_tasks: BackgroundTasks,
    ) -> type[Menu]:
        item = await self.repository.update_menu(menu_id, menu_schema)
        background_tasks.add_task(self.cache.invalidate, "menu", f"menu_{menu_id}")
        return item

    async def delete(
        self,
        menu_id: UUID4,
        background_tasks: BackgroundTasks,
    ) -> None:
        item = await self.repository.delete(menu_id)
        background_tasks.add_task(self.cache.invalidate, "menu", f"menu_{menu_id}*")

    async def count(self, menu_id: UUID4) -> MenuExtended:
        return await self.cache.fetch(
            f"menu_{menu_id}_count", self.get_complex_query, menu_id
        )

    async def get_complex_query(self, menu_id: UUID4) -> MenuExtended:
        result = await self.repository.get_complex_query(menu_id)
        try:
            menu, submenu_count, dishes_count = result
        except TypeError:
            raise MenuExistsException()
        menu_dict = {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenu_count,
            "dishes_count": dishes_count,
        }
        return menu_dict
