
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database.exceptions import SubmenuExistsException
from app.database.models import Dishes, Submenu
from app.database.schemas import SubmenuCreate, SubmenuUpdate


def get_sub(db: Session, menu_id: UUID4, submenu_id: UUID4):
    submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
    if not submenu:
        raise SubmenuExistsException()
    result = jsonable_encoder(submenu)
    dishes = db.query(Dishes).filter(Dishes.submenu_id==submenu_id).all()
    if not dishes:
        result['dishes_count'] = 0
    else:
        result['dishes_count'] = len(dishes)
    return result


def get_submenu_list(db: Session, id: UUID4):
    try:
        all_submenu = db.query(Submenu).filter(Submenu.menu_id == id).all()
    except:
        all_submenu = []
    return all_submenu


def create_submenu(db: Session, menu_id: UUID4, submenu: SubmenuCreate):
    new_submenu = Submenu(**submenu.model_dump())
    new_submenu.dishes_count = 0
    new_submenu.menu_id = menu_id
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


def update_submenu(db: Session, menu_id: UUID4, submenu_id: UUID4, update_submenu: SubmenuUpdate):
    db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
    if not db_submenu:
        raise SubmenuExistsException()
    else:
        db_submenu.title = update_submenu.title
        db_submenu.description = update_submenu.description
        db.add(db_submenu)
        db.commit()
        db.refresh(db_submenu)
    return db_submenu


def delete_submenu(db: Session, menu_id: UUID4, submenu_id: UUID4):
    db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
    db.delete(db_submenu)
    db.commit()
