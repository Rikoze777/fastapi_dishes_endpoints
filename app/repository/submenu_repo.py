from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.future import select

from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Submenu
from app.repository.exceptions import SubmenuExistsException
from app.schemas.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuRepositary:
    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_sub(self, menu_id: UUID4, submenu_id: UUID4) -> Submenu:
        async with self.async_session.begin() as db_session:
            stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
            result = await db_session.execute(stmt)
            submenu = result.scalars().first()
            if not submenu:
                raise SubmenuExistsException()
            result = jsonable_encoder(submenu)
            return result

    async def get_submenu_list(self, menu_id: UUID4) -> list[Submenu]:
        async with self.async_session.begin() as db_session:
            stmt = select(Submenu).filter_by(menu_id=menu_id)
            result = await db_session.execute(stmt)
            all_submenu = result.scalars().all()
            return all_submenu

    async def create_submenu(self, menu_id: UUID4, submenu: SubmenuCreate) -> Submenu:
        async with self.async_session.begin() as db_session:
            new_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
            db_session.add(new_submenu)
            await db_session.flush()
            await db_session.refresh(new_submenu)
            return new_submenu

    async def update_submenu(
        self, menu_id: UUID4, submenu_id: UUID4, update_submenu: SubmenuUpdate
    ) -> Submenu:
        async with self.async_session.begin() as db_session:
            stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
            result = await db_session.execute(stmt)
            db_submenu = result.scalars().first()
            if not db_submenu:
                raise SubmenuExistsException()
            db_submenu.title = update_submenu.title
            db_submenu.description = update_submenu.description
            await db_session.flush()
            await db_session.refresh(db_submenu)
            return db_submenu

    async def delete_submenu(self, menu_id: UUID4, submenu_id: UUID4) -> None:
        async with self.async_session.begin() as db_session:
            stmt = select(Submenu).filter_by(menu_id=menu_id, id=submenu_id)
            result = await db_session.execute(stmt)
            db_submenu = result.scalars().first()
            await db_session.delete(db_submenu)
            await db_session.commit()
