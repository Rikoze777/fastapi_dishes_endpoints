from fastapi import BackgroundTasks, Depends
from pydantic import UUID4

from app.cache.redis import cache_instance
from app.database.models import Submenu
from app.repository.submenu_repo import SubmenuRepositary
from app.schemas import schemas


class SubmenuService:
    def __init__(self, repository: SubmenuRepositary = Depends()):
        self.repository = repository
        self.cache = cache_instance

    async def get_submenu_list(self, menu_id: UUID4) -> list[Submenu]:
        return await self.cache.fetch(
            f'menu_{menu_id}_submenu',
            self.repository.get_submenu_list,
            menu_id,
        )

    async def get(self, menu_id: UUID4, submenu_id: UUID4) -> Submenu:
        return await self.cache.fetch(
            f'menu_{menu_id}_submenu_{submenu_id}',
            self.repository.get_sub,
            menu_id,
            submenu_id,
        )

    async def create(
        self,
        menu_id: UUID4,
        schema: schemas.SubmenuCreate,
        background_tasks: BackgroundTasks,
    ) -> Submenu:
        menu = await self.repository.create_submenu(menu_id, schema)
        background_tasks.add_task(self.cache.invalidate, f'menu_{menu_id}_submenu')
        return menu

    async def update(
        self,
        menu_id: UUID4,
        submenu_id: UUID4,
        schema: schemas.SubmenuUpdate,
        background_tasks: BackgroundTasks,
    ) -> type[Submenu]:
        item = await self.repository.update_submenu(menu_id, submenu_id, schema)
        background_tasks.add_task(
            self.cache.invalidate,
            f'menu_{menu_id}_submenu',
            f'menu_{menu_id}_submenu_{submenu_id}',
        )
        return item

    async def delete(
        self,
        menu_id: UUID4,
        submenu_id: UUID4,
        background_tasks: BackgroundTasks,
    ) -> None:
        await self.repository.delete_submenu(menu_id, submenu_id)
        background_tasks.add_task(
            self.cache.invalidate,
            f'menu_{menu_id}_submenu',
            f'menu_{menu_id}_submenu_{submenu_id}*',
        )
