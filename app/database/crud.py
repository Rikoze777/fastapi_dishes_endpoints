from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .models import Menu
from .schemas import MenuCreate
from utils.exceptions import MenuException


def get_menu(db: Session, id: str):
    menu = db.query(Menu).filter(Menu.id == id).first()
    if not menu:
        raise MenuException(id)
    result = jsonable_encoder(menu)
    result['submenus_count'] = 0
    result['dishes_count'] = 0
    return result


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
    return new_menu


def update_menu(db: Session, id: str, update_menu: MenuCreate):
    db_menu = db.query(Menu).filter(Menu.id == id).first()
    db_menu.title = update_menu.title
    db_menu.description = update_menu.description
    db.add(db_menu)
    db.commit()
    return db_menu


def delete_menu(db: Session, id: str):
    db_menu = db.query(Menu).filter(Menu.id == id).first()
    db.delete(db_menu)
    db.commit()
