from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException
import uuid
from app.schemas import schemas
from app.database.db import get_db
from app.services.menu import MenuService


router = APIRouter(
    tags=["menu"],
    prefix="/api/v1",
)


@router.get(
    "/menus",
    response_model=List[schemas.Menu],
    name="Список меню",
)
def get_menu_list(menu: MenuService = Depends()):
    return menu.get_menu_list()


@router.post(
    "/menus",
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: schemas.MenuCreate, menu: MenuService = Depends()):
    result = menu.create_menu(data)
    return menu.get_menu(result.id)


@router.get(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Меню по id",
)
def get_menu(id: UUID4, menu: MenuService = Depends()):
    try:
        menu = menu.get_menu(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.patch(
    "/menus/{id}/",
    response_model=schemas.Menu,
    name="Обновить меню",
)
def update_menu(id: UUID4,
                data: schemas.MenuUpdate,
                menu: MenuService = Depends()):
    menu.get_menu(id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu.update_menu(id, data)


@router.delete(
    "/menus/{id}/",
    name="Удалить меню",
)
def delete_menu(id: UUID4, menu: MenuService = Depends()):
    menu.delete_menu(id)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Menu has been deleted"}
    )


@router.get(
        "/menus/{id}/count",
        name="Посчитать подменю и блюда")
def get_menu_counts(id: UUID4, menu: MenuService = Depends()):
    menus = menu.get_complex_query(id)

    menu, submenu_count, dishes_count = menus
    menu_dict = {
        "id": id,
        "title": menu.title,
        "description": menu.description,
        "submenus_count": submenu_count,
        "dishes_count": dishes_count,
    }

    return menu_dict
