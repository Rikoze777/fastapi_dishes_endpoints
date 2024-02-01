from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from app.crud.exceptions import SubmenuExistsException
from app.database.models import Dishes, Submenu
from app.schemas.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_sub(self,
                      menu_id: UUID4,
                      submenu_id: UUID4) -> Submenu:
        stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
        result = await self.db.execute(stmt)
        submenu = result.scalars().first()
        if not submenu:
            raise SubmenuExistsException()
        result = jsonable_encoder(submenu)
        stmt = select(Dishes).filter_by(submenu_id=submenu_id)
        dishes_result = await self.db.execute(stmt)
        dishes = dishes_result.scalars().all()
        result['dishes_count'] = len(dishes)
        return result

    async def get_submenu_list(self,
                               menu_id: UUID4) -> List[Submenu]:
        stmt = select(Submenu).filter_by(menu_id=menu_id)
        result = await self.db.execute(stmt)
        all_submenu = result.scalars().all()
        return all_submenu

    async def create_submenu(self,
                             menu_id: UUID4,
                             submenu: SubmenuCreate) -> Submenu:
        new_submenu = Submenu(**submenu.model_dump(),
                              menu_id=menu_id)
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def update_submenu(self,
                             menu_id: UUID4,
                             submenu_id: UUID4,
                             update_submenu: SubmenuUpdate) -> Submenu:
        stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
        result = await self.db.execute(stmt)
        db_submenu = result.scalars().first()
        if not db_submenu:
            raise SubmenuExistsException()
        db_submenu.title = update_submenu.title
        db_submenu.description = update_submenu.description
        await self.db.commit()
        await self.db.refresh(db_submenu)
        return db_submenu

    async def delete_submenu(self,
                             menu_id: UUID4,
                             submenu_id: UUID4) -> None:
        stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
        result = await self.db.execute(stmt)
        db_submenu = result.scalars().first()
        await self.db.delete(db_submenu)
        await self.db.commit()
