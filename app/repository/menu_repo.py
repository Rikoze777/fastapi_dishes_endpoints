from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.sql import label
from sqlalchemy.orm import selectinload
from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Dishes, Menu, Submenu
from app.repository.exceptions import MenuExistsException
from app.schemas.schemas import MenuCreate, MenuItem, MenuUpdate, Menu as MenuModel


class MenuRepository:

    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_menu(self, id: UUID4) -> MenuModel:
        return await self.__get_complex_menu(id)

    async def __get_complex_menu(self, menu_id: UUID4) -> MenuModel:
        async with self.async_session.begin() as db_session:
            statement = (
                select(
                    Menu,
                    label("submenu_count", func.count(Submenu.id.distinct())),
                    label("dishes_count", func.count(Dishes.id)),
                )
                .filter(Menu.id == menu_id)
                .outerjoin(Submenu, Menu.id == Submenu.menu_id)
                .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
                .group_by(Menu)
            )
            result = await db_session.execute(statement)
            try:
                menu, submenu_count, dishes_count = result.first()
            except TypeError:
                raise MenuExistsException()
            menu_dict = {
                "id": menu.id,
                "title": menu.title,
                "description": menu.description,
                "submenus_count": submenu_count,
                "dishes_count": dishes_count,
            }
            return MenuModel.model_validate(menu_dict)

    async def get_menu_list(self) -> list[MenuItem]:
        async with self.async_session.begin() as db_session:
            menus = await db_session.execute(select(Menu))
            menus = menus.scalars().all()
            if not menus:
                return []
            result = list(map(MenuModel.model_validate, menus))
            return result

    async def create_menu(self, menu: MenuCreate) -> MenuModel:
        async with self.async_session.begin() as db_session:
            new_menu = Menu(**menu.model_dump())
            db_session.add(new_menu)
            await db_session.flush()
            await db_session.refresh(new_menu)
            return MenuModel.model_validate(new_menu)

    async def update_menu(self, id: UUID4, update_menu: MenuUpdate) -> MenuModel:
        async with self.async_session.begin() as db_session:
            db_menu = await db_session.get(Menu, id)
            db_menu.title = update_menu.title
            db_menu.description = update_menu.description
            db_session.add(db_menu)
            await db_session.flush()
            await db_session.refresh(db_menu)
            return MenuModel.model_validate(db_menu)

    async def delete(self, id: UUID4) -> None:
        async with self.async_session.begin() as db_session:
            db_menu = await db_session.get(Menu, id)
            await db_session.delete(db_menu)
            await db_session.commit()

    async def get_all_menus(self):
        async with self.async_session.begin() as db_session:
            menus = select(Menu).options(
                selectinload(Menu.submenus).selectinload(Submenu.dishes)
            )
        result = await db_session.execute(menus)
        result = result.scalars().all()
        if not result:
            return []
        return result
