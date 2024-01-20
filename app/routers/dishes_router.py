from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import dishes_crud, schemas
from database.db import get_db
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
def get_dishes_list(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    return dishes_crud.get_dishes_list(db, submenu_id)


# Просмотр определенного блюда
@router.get(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Блюдо по id",
)
def get_dish(submenu_id: int, id: int, db: Session = Depends(get_db)):
    dish = dishes_crud.get_dish(db, submenu_id, id)
    if not dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    return dish


# Создать блюдо
@router.post(
    "/dishes",
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(menu_id: int, submenu_id: int, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = dishes_crud.create_dish(db, submenu_id, data)
    return dishes_crud.get_dish(db, submenu_id, dish.id)


# Обновить блюдо
@router.patch(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Обновить блюдо",
)
def update_dish(menu_id: int, submenu_id: int, id: int, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = dishes_crud.get_dish(db, submenu_id, id)
    if not dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    update_dish = dishes_crud.update_dish(db, submenu_id, id, data)
    return dishes_crud.get_dish(db, submenu_id, update_dish.id)


# Удаление блюда
@router.delete(
    "/dishes/{id}",
    name="Удалить блюдо",
)
def delete_dish(menu_id: int, submenu_id: int, id: int, db: Session = Depends(get_db)):
    dishes_crud.delete_dish(db, submenu_id, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )