from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from .models import Dishes
from .schemas import Dishes, DishesCreate
from fastapi import HTTPException


def get_dish(db: Session, submenu_id: str, id: str):
    dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return dish


# Создать блюдо
def create_dish(db: Session, submenu_id: str, dish: DishesCreate):
    new_dish = Dishes(**dish.model_dump())
    new_dish.price = round(dish.price, 2)
    new_dish.submenu_id = submenu_id
    db.add(new_dish)
    db.commit()
    return new_dish


# Обновить блюдо
def update_dish(db: Session, submenu_id: str, id: str, update_dish: DishesCreate):
    db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    else:
        db_dish.title = update_dish.title
        db_dish.description = update_dish.description
        db_dish.price = round(update_dish.price, 2)
        db.add(db_dish)
        db.commit()
    return db_dish


# Просмотр списка блюд
def get_dishes_list(db: Session, submenu_id: str):
    all_dishes = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).all()
    if not all_dishes:
        return []
    else:
        list_dishes = [get_dish(db, submenu_id, dish.id) for dish in all_dishes]
        return list_dishes


# Удаление блюда
def delete_dish(db: Session, submenu_id: str, id: str):
    db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
    db.delete(db_dish)
    db.commit()