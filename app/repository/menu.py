from sqlalchemy.future import select
from sqlalchemy import func, label
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Dishes, Menu, Submenu
from app.schemas.schemas import MenuCreate, MenuUpdate
from fastapi.encoders import jsonable_encoder


class MenuRepository:

    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_menu(self,
                       id: UUID4) -> Menu:
        async with self.async_session.begin() as session:
            menu = await session.get(Menu, id)
            if not menu:
                raise MenuExistsException()
            result = jsonable_encoder(menu)
            return result

    async def get_complex_query(self,
                                menu_id: UUID4):
        async with self.async_session.begin() as session:
            statement = (
                select(
                    Menu,
                    label("submenu_count", func.count(Submenu.id.distinct())),
                    label("dishes_count", func.count(Dishes.id))
                )
                .filter(Menu.id == menu_id)
                .outerjoin(Submenu, Menu.id == Submenu.menu_id)
                .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
                .group_by(Menu.id)
            )
            result = await session.execute(statement)
            return result.first()

    async def get_menu_list(self) -> list[Menu]:
        async with self.async_session.begin() as session:
            menus = await session.execute(select(Menu))
            menus = menus.scalars().all()
            if not menus:
                return []
            else:
                list_menu = [await self.get_menu(menu.id) for menu in menus]
                return list_menu

    async def create_menu(self,
                          menu: MenuCreate) -> Menu:
        session: AsyncSession
        async with self.async_session.begin() as session:
            new_menu = Menu(**menu.model_dump())
            session.add(new_menu)
            await session.flush()
            await session.refresh(new_menu)
            return new_menu

    async def update_menu(self,
                          id: UUID4,
                          update_menu: MenuUpdate) -> Menu:
        async with self.async_session.begin() as session:
            db_menu = await session.get(Menu, id)
            db_menu.title = update_menu.title
            db_menu.description = update_menu.description
            session.add(db_menu)
            await session.flush()
            await session.refresh(db_menu)
            return db_menu

    async def delete(self,
                     id: UUID4) -> None:
        async with self.async_session.begin() as session:
            db_menu = await session.get(Menu, id)
            await session.delete(db_menu)
            await session.commit()
