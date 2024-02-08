from typing import List
from fastapi import BackgroundTasks, Depends
from pydantic import UUID4
from app.repository.dish import DishRepository
from app.cache.redis import cache_instance
from app.schemas.schemas import Dishes, DishesCreate, DishesUpdate, Submenu, SubmenuCreate, SubmenuUpdate


class DishService:

    def __init__(self, repository: DishRepository = Depends()):
        self.repository = repository
        self.cache = cache_instance

    async def get_dishes_list(self, menu_id: UUID4, submenu_id: UUID4) -> List[Dishes]:
        return await self.cache.fetch(f"menu_{menu_id}_submenu_{submenu_id}_dish", self.repository.get_dishes_list, submenu_id,)

    async def get(self, menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4) -> Dishes:
        return await self.cache.fetch(f"menu_{menu_id}_submenu_{submenu_id}_dish_{dish_id}",
                                      self.repository.get_dish,
                                      submenu_id,
                                      dish_id,)

    async def create(self,
                     menu_id: UUID4,
                     submenu_id: UUID4,
                     schema: DishesCreate,
                     background_tasks: BackgroundTasks,) -> Dishes:
        menu = await self.repository.create_dish(submenu_id, schema)
        background_tasks.add_task(self.cache.invalidate, f"menu_{menu_id}_submenu_{submenu_id}_dish")
        return menu

    async def update(self,
                     menu_id: UUID4,
                     submenu_id: UUID4,
                     dish_id: UUID4,
                     schema: DishesUpdate,
                     background_tasks: BackgroundTasks,) -> type[Dishes]:
        item = await self.repository.update_dish(submenu_id, dish_id, schema)
        background_tasks.add_task(
            self.cache.invalidate,
            f"menu_{menu_id}_submenu_{submenu_id}_dish",
            f"menu_{menu_id}_submenu_{submenu_id}_dish_{dish_id}",
        )
        return item

    async def delete(self,
                     menu_id: UUID4,
                     submenu_id: UUID4,
                     dish_id: UUID4,
                     background_tasks: BackgroundTasks,) -> None:
        await self.repository.delete_dish(submenu_id, dish_id)
        background_tasks.add_task(
            self.cache.invalidate,
            f"menu_{menu_id}_submenu_{submenu_id}_dish",
            f"menu_{menu_id}_submenu_{submenu_id}_dish_{dish_id}*",
        )