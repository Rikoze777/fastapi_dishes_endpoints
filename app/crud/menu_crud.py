from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.sql import label
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException
from app.database.models import Dishes, Menu, Submenu
from app.schemas.schemas import MenuCreate, MenuUpdate


def get_menu(db: Session, id: UUID4):
    menu = db.query(Menu).get(id)
    if not menu:
        raise MenuExistsException()
    result = jsonable_encoder(menu)
    submenus = db.query(Submenu).filter(Submenu.menu_id == id).all()
    if not submenus:
        result['submenus_count'] = 0
        result['dishes_count'] = 0
    else:
        result['submenus_count'] = len(submenus)
        for submenu in submenus:
            dishes = db.query(Dishes).filter(Dishes.submenu_id == submenu.id).all()
            if not dishes:
                result['dishes_count'] = 0
            else:
                result['dishes_count'] = len(dishes)
    return result


def get_complex_query(db: Session, menu_id: UUID4):

    menus = (
        db.query(
            Menu,
            label("submenu_count", func.count(Submenu.id.distinct())),
            label("dishes_count", func.count(Dishes.id))
        )
        .filter(Menu.id == menu_id)
        .outerjoin(Submenu, Menu.id == Submenu.menu_id)
        .outerjoin(Dishes, Submenu.id == Dishes.submenu_id)
        .group_by(Menu.id)
        .first()
    )
    return menus


def get_menu_list(db: Session):
    all_menu = db.query(Menu).all()
    if not all_menu:
        return []
    else:
        list_menu = [get_menu(db, menu.id) for menu in all_menu]
        return list_menu


def create_menu(db: Session, menu: MenuCreate):
    new_menu = Menu(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def update_menu(db: Session, id: UUID4, update_menu: MenuUpdate):
    db_menu = db.query(Menu).filter(Menu.id == id).first()
    db_menu.title = update_menu.title
    db_menu.description = update_menu.description
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, id: UUID4):
    db_menu = db.query(Menu).filter(Menu.id == id).first()
    db.delete(db_menu)
    db.commit()
