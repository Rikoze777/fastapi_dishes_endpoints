from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, label
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException
from app.database.models import Dishes, Menu, Submenu
from app.schemas.schemas import MenuCreate, MenuUpdate
from fastapi.encoders import jsonable_encoder


class MenuRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_menu(self,
                       id: UUID4) -> Menu:
        menu = await self.db.get(Menu, id)
        if not menu:
            raise MenuExistsException()
        result = jsonable_encoder(menu)
        submenus = await self.db.execute(select(Submenu).filter(Submenu.menu_id == id))
        submenus = submenus.scalars().all()
        if not submenus:
            result['submenus_count'] = 0
            result['dishes_count'] = 0
        else:
            result['submenus_count'] = len(submenus)
            for submenu in submenus:
                dishes = await self.db.execute(select(Dishes).filter(Dishes.submenu_id == submenu.id))
                dishes = dishes.scalars().all()
                if not dishes:
                    result['dishes_count'] = 0
                else:
                    result['dishes_count'] = len(dishes)
        return result

    async def get_complex_query(self,
                                menu_id: UUID4) -> Menu:
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
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def get_menu_list(self) -> list[Menu]:
        menus = await self.db.execute(select(Menu))
        menus = menus.scalars().all()
        if not menus:
            return []
        else:
            list_menu = [await self.get_menu(menu.id) for menu in menus]
            return list_menu

    async def create_menu(self,
                          menu: MenuCreate) -> Menu:
        new_menu = Menu(**menu.model_dump())
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def update_menu(self,
                          id: UUID4,
                          update_menu: MenuUpdate) -> Menu:
        db_menu = await self.db.get(Menu, id)
        db_menu.title = update_menu.title
        db_menu.description = update_menu.description
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        return db_menu

    async def delete_menu(self,
                          id: UUID4) -> None:
        db_menu = await self.db.get(Menu, id)
        await self.db.delete(db_menu)
        await self.db.commit()
