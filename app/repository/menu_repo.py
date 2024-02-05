from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import label

from app.database.db import get_db
from app.database.models import Dishes, Menu, Submenu
from app.repository.exceptions import MenuExistsException
from app.schemas.schemas import MenuCreate, MenuUpdate


class MenuRepositary:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_menu(self, id: UUID4):
        menu = self.session.query(Menu).get(id)
        if not menu:
            raise MenuExistsException()
        result = jsonable_encoder(menu)
        submenus = self.session.query(Submenu)\
                               .filter(Submenu.menu_id == id)\
                               .all()
        if not submenus:
            result['submenus_count'] = 0
            result['dishes_count'] = 0
        else:
            result['submenus_count'] = len(submenus)
            for submenu in submenus:
                dishes = self.session.query(Dishes)\
                                     .filter(Dishes.submenu_id == submenu.id)\
                                     .all()
                if not dishes:
                    result['dishes_count'] = 0
                else:
                    result['dishes_count'] = len(dishes)
        return result

    def get_complex_query(self, menu_id: UUID4):

        menus = (
            self.session.query(
                Menu,
                label('submenu_count', func.count(Submenu.id.distinct())),
                label('dishes_count', func.count(Dishes.id))
            )
            .filter(Menu.id == menu_id)
            .outerjoin(Submenu, Menu.id == Submenu.menu_id)
            .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
            .group_by(Menu.id)
            .first()
        )
        return menus

    def get_menu_list(self):
        all_menu = self.session.query(Menu).all()
        if not all_menu:
            return []
        else:
            list_menu = [self.get_menu(menu.id) for menu in all_menu]
            return list_menu

    def create_menu(self, menu: MenuCreate):
        new_menu = Menu(**menu.model_dump())
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def update_menu(self, id: UUID4, update_menu: MenuUpdate):
        db_menu = self.session.query(Menu).filter(Menu.id == id).first()
        db_menu.title = update_menu.title
        db_menu.description = update_menu.description
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def delete_menu(self, id: UUID4):
        db_menu = self.session.query(Menu).filter(Menu.id == id).first()
        self.session.delete(db_menu)
        self.session.commit()
