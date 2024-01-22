from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import UUID4
from app.database.exceptions import DishExistsException
from app.database.models import Dishes
from app.database.schemas import DishesUpdate, DishesCreate


def get_dish(db: Session, submenu_id: UUID4, id: UUID4):
    dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    if not dish:
        raise DishExistsException()
    return dish


def create_dish(db: Session, submenu_id: UUID4, dish: DishesCreate):
    new_dish = Dishes(**dish.dict())
    new_dish.submenu_id = submenu_id
    new_dish.price = new_dish.price
    # "{:.2f}".format(float(new_dish.price))
    db.add(new_dish)
    db.commit()
    return new_dish


def update_dish(db: Session, submenu_id: UUID4, id: UUID4, update_dish: DishesUpdate):
    db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    if not db_dish:
        raise DishExistsException()
    else:
        db_dish.title = update_dish.title
        db_dish.description = update_dish.description
        db_dish.price = update_dish.price
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
    return db_dish


def get_dishes_list(db: Session, submenu_id: UUID4):
    all_dishes = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).all()
    if not all_dishes:
        return []
    else:
        list_dishes = [get_dish(db, submenu_id, dish.id) for dish in all_dishes]
        return list_dishes


def delete_dish(db: Session, submenu_id: UUID4, id: UUID4):
    db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    db.delete(db_dish)
    db.commit()
