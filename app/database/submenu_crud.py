from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .models import Submenu
from .schemas import SubmenuCreate, SubmenuUpdate
from fastapi import HTTPException


def get_submenu(db: Session, menu_id: str, submenu_id: str):
    submenu = db.query(Submenu).filter(menu_id == menu_id).filter(id == submenu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    result = jsonable_encoder(submenu)
    result['dishes_count'] = 0


def get_submenu_list(db: Session, menu_id: str):
    all_submenu = db.query(Submenu).filter(menu_id == menu_id).all()
    if not all_submenu:
        return []
    else:
        list_submenu = [get_submenu(db, menu_id, submenu.id) for submenu in all_submenu]
        return list_submenu


def create_submenu(db: Session, menu_id: str, submenu: SubmenuCreate):
    new_submenu = Submenu(**submenu.model_dump())
    new_submenu.menu_id = menu_id
    new_submenu.dishes_count = 0
    new_submenu
    db.add(new_submenu)
    db.commit()
    return new_submenu


def update_submenu(db: Session, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate):
    db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    else:
        db_submenu.title = update_submenu.title
        db_submenu.description = update_submenu.description
        db.add(db_submenu)
        db.commit()
    return db_submenu


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
    db.delete(db_submenu)
    db.commit()
