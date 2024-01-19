from fastapi import APIRouter
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from database import crud, schemas
from database.db import get_db
from fastapi.responses import JSONResponse
from utils.exceptions import MenuException


router = APIRouter(
)


@router.get(
    "/api/v1/menus",
    response_model=List[schemas.Menu],
    name="Список меню",
)
def get_menu_list(db: Session = Depends(get_db)):
    return crud.get_menu_list(db)


@router.post(
    "/api/v1/menus",
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = crud.create_menu(db, data)
    return crud.get_menu(db, menu.id)


@router.get(
    "/api/v1/menus/{id}/",
    response_model=schemas.Menu,
    name="Меню по id",
)
def get_menu(id: str, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuException()
    return menu


@router.patch(
    "/api/v1/menus/{id}/",
    response_model=schemas.Menu,
    name="Обновить меню",
)
def update_menu(id: str, data: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = crud.get_menu(db, id)
    if not menu:
        raise MenuException()
    update_menu = crud.update_menu(db, id, data)
    return crud.get_menu(db, update_menu.id)


@router.delete(
    "/api/v1/menus/{id}/",
    name="Удалить меню",
)
def delete_menu(id: str, db: Session = Depends(get_db)):
    crud.delete_menu(db, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Menu has been deleted"}
    )
