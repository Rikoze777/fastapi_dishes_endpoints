from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.sql import label

from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Dishes, Menu, Submenu
from app.repository.exceptions import MenuExistsException
from app.schemas.schemas import MenuCreate, MenuUpdate


class MenuRepository:

    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_menu(self, id: UUID4) -> Menu:
        async with self.async_session.begin() as db_session:
            menu = await db_session.get(Menu, id)
            if not menu:
                raise MenuExistsException()
            result = jsonable_encoder(menu)
            submenus_select = select(Submenu).filter(Submenu.menu_id == id)
            sub = await db_session.execute(submenus_select)
            submenus = sub.scalars()
            if not submenus:
                result['submenus_count'] = 0
                result['dishes_count'] = 0
            else:
                result['submenus_count'] = len(submenus)
                for submenu in submenus:
                    dishes_select = select(Dishes).filter(
                        Dishes.submenu_id == submenu.id
                    )
                    dish = await db_session.execute(dishes_select)
                    dishes = dish.scalars()
                    if not dishes:
                        result['dishes_count'] = 0
                    else:
                        result['dishes_count'] = len(dishes)
            return result

    async def get_complex_query(self, menu_id: UUID4):
        async with self.async_session.begin() as db_session:
            statement = (
                select(
                    Menu,
                    label('submenu_count', func.count(Submenu.id.distinct())),
                    label('dishes_count', func.count(Dishes.id)),
                )
                .filter(Menu.id == menu_id)
                .outerjoin(Submenu, Menu.id == Submenu.menu_id)
                .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
                .group_by(Menu.id)
            )
            result = await db_session.execute(statement)
            return result.first()

    async def get_menu_list(self) -> list[Menu]:
        async with self.async_session.begin() as db_session:
            menus = await db_session.execute(select(Menu))
            menus = menus.scalars().all()
            if not menus:
                return []
            else:
                list_menu = [await self.get_menu(menu.id) for menu in menus]
                return list_menu

    async def create_menu(self, menu: MenuCreate) -> Menu:
        async with self.async_session.begin() as db_session:
            new_menu = Menu(**menu.model_dump())
            db_session.add(new_menu)
            await db_session.flush()
            await db_session.refresh(new_menu)
            return new_menu

    async def update_menu(self, id: UUID4, update_menu: MenuUpdate) -> Menu:
        async with self.async_session.begin() as db_session:
            db_menu = await db_session.get(Menu, id)
            db_menu.title = update_menu.title
            db_menu.description = update_menu.description
            db_session.add(db_menu)
            await db_session.flush()
            await db_session.refresh(db_menu)
            return db_menu

    async def delete(self, id: UUID4) -> None:
        async with self.async_session.begin() as db_session:
            db_menu = await db_session.get(Menu, id)
            await db_session.delete(db_menu)
            await db_session.commit()
