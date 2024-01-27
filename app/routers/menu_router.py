from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.crud import menu_crud
from app.schemas import schemas
from app.database.db import get_db


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
    return menu_crud.get_menu_list(db)


@router.post(
    "/menus",
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: schemas.MenuCreate, db: Session = Depends(get_db)):
    menu = menu_crud.create_menu(db, data)
    return menu_crud.get_menu(db, menu.id)


@router.get(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Меню по id",
)
def get_menu(id: UUID4, db: Session = Depends(get_db)):
    try:
        menu = menu_crud.get_menu(db, id)
    except:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.patch(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Обновить меню",
)
def update_menu(id: UUID4, data: schemas.MenuUpdate, db: Session = Depends(get_db)):
    menu = menu_crud.get_menu(db, id)
    if not menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    update_menu = menu_crud.update_menu(db, id, data)
    return menu_crud.get_menu(db, update_menu.id)


@router.delete(
    "/menus/{id}/",
    name="Удалить меню",
)
def delete_menu(id: UUID4, db: Session = Depends(get_db)):
    menu_crud.delete_menu(db, id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Menu has been deleted"}
    )


@router.get(
        "/menu_counts",)
def get_menu_counts(menu_id: UUID4, db: Session = Depends(get_db)):
    menus = menu_crud.get_complex_query(db, menu_id)

    menu, submenu_count, dishes_count = menus
    menu_dict = {
        "menu_id": str(menu.id),
        "title": menu.title,
        "description": menu.description,
        "submenu_count": submenu_count,
        "dishes_count": dishes_count,
    }

    return menu_dict
