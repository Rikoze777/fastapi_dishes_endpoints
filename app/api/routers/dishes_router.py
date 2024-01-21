from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api import schemas
from app.database.dishes_crud import DishesStorage
from app.database.db import get_db
from fastapi.responses import JSONResponse


router = APIRouter(
    tags=["dishes"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
)


@router.get(
    "/dishes",
    response_model=List[schemas.Dishes],
    name="Список блюд",
)
def get_dishes_list(submenu_id: UUID, db: Session = Depends(get_db)):
    return DishesStorage.get_list_dishes(db, submenu_id)


# Просмотр определенного блюда
@router.get(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Блюдо по id",
)
def get_dish(submenu_id: UUID, id: UUID, db: Session = Depends(get_db)):
    dish = DishesStorage.get_dish(db, submenu_id, id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


# Создать блюдо
@router.post(
    "/dishes",
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(menu_id: UUID, submenu_id: UUID, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = DishesStorage.create_dish(db, submenu_id, data)
    return DishesStorage.get_dish(db, submenu_id, dish.id)


# Обновить блюдо
@router.patch(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Обновить блюдо",
)
def update_dish(menu_id: UUID, submenu_id: UUID, id: UUID, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = DishesStorage.get_dish(db, submenu_id, id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    update_dish = DishesStorage.update_dish(db, submenu_id, id, data)
    return DishesStorage.get_dish(db, submenu_id, update_dish.id)


# Удаление блюда
@router.delete(
    "/dishes/{id}",
    name="Удалить блюдо",
)
def delete_dish(menu_id: int, submenu_id: int, id: int, db: Session = Depends(get_db)):
    DishesStorage.delete_dish(db, submenu_id, id)
    return JSONResponse(
        status_code=204,
        content={"status": "true", "message": "The dish has been deleted"}
    )