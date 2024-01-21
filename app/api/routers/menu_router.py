from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api import schemas
from app.database.menu_crud import MenuStorage
from app.database.db import get_db
from fastapi.responses import JSONResponse


router = APIRouter(
    tags=["menu"],
    prefix="/api/v1",
)


@router.get(
    "/menus",
    response_model=List[schemas.Menu],
    name="Список меню",
)
def get_menu_list(db: Session = Depends(get_db)):
    return MenuStorage.get_list_menus(db)


@router.post(
    "/menus",
    response_model=schemas.MenuCreate,
    name='Создать меню',
    status_code=201,
)
def add_menu(id: str, db: Session = Depends(get_db)):
    menu = MenuStorage.create_menu(id, db)
    return menu


@router.get(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Меню по id",
)
def get_menu(id: str, db: Session = Depends(get_db)):
    menu = MenuStorage.get_menu(id, db)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.patch(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Обновить меню",
)
def update_menu(id: str, data: schemas.MenuUpdate, db: Session = Depends(get_db)):
    menu = MenuStorage.get_menu(db, id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    update_menu = MenuStorage.update_menu(db, id, data)
    return MenuStorage.get_menu(db, update_menu.id)


@router.delete(
    "/menus/{id}/",
    name="Удалить меню",
)
def delete_menu(id: str, db: Session = Depends(get_db)):
    MenuStorage.delete_menu(db, id)
    return JSONResponse(
        status_code=204,
        content={"status": "true", "message": "Menu has been deleted"}
    )
