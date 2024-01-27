from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud import dishes_crud
from app.database.db import get_db
from fastapi.responses import JSONResponse
from pydantic import UUID4


router = APIRouter(
    tags=["dishes"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
)


@router.get(
    "/dishes",
    response_model=List[schemas.Dishes],
    name="Список блюд",
)
def get_dishes_list(menu_id: UUID4, submenu_id: UUID4, db: Session = Depends(get_db)):
    dishes_list = dishes_crud.get_dishes_list(db, submenu_id)
    for dish in dishes_list:
        dish.price = "{:.2f}".format(float(dish.price))
    return dishes_list


@router.get(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Блюдо по id",
)
def get_dish(submenu_id: UUID4, id: UUID4, db: Session = Depends(get_db)):
    try:
        dish = dishes_crud.get_dish(db, submenu_id, id)
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    dish.price = "{:.2f}".format(float(dish.price))
    return dish


@router.post(
    "/dishes",
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(submenu_id: UUID4, data: schemas.DishesCreate, db: Session = Depends(get_db)):
    dish = dishes_crud.create_dish(db, submenu_id, data)
    dish.price = str("{:.2f}".format(float(dish.price)))
    return dish


@router.patch(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Обновить блюдо",
)
def update_dish(submenu_id: UUID4, id: UUID4, data: schemas.DishesUpdate, db: Session = Depends(get_db)):
    try:
        dish = dishes_crud.get_dish(db, submenu_id, id)
        updated_dish = dishes_crud.update_dish(db, submenu_id, id, data)
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    updated_dish.price = str("{:.2f}".format(float(dish.price)))
    return dish


@router.delete(
    "/dishes/{id}",
    name="Удалить блюдо",
)
def delete_dish(submenu_id: UUID4, id: UUID4, db: Session = Depends(get_db)):
    dishes_crud.delete_dish(db, submenu_id, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )
