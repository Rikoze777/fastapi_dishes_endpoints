from tkinter import Menu
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException

from app.services.menu_service import MenuService
from app.schemas import schemas
from app.database.db import get_async_session


router = APIRouter(
    tags=["menu"],
    prefix="/api/v1/menus",
)


@router.get(
    "/",
    response_model=List[schemas.Menu],
    name="Список меню",
)
async def get_menu_list(menu: MenuService = Depends()) -> List[Menu]:
    return await menu.get_menu_list()


@router.post(
    "/",
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=201,
)
async def add_menu(data: schemas.MenuCreate,
                   background_tasks: BackgroundTasks,
                   menu: MenuService = Depends(),) -> Menu:
    return await menu.create(data, background_tasks)


@router.get(
    "/{id}/",
    response_model=schemas.Menu,
    name="Меню по id",
)
def get_menu(id: UUID4, menu: MenuService = Depends()) -> Menu:
    try:
        result = menu.get(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail="menu not found")
    return result


@router.patch(
    "/{id}/",
    response_model=schemas.Menu,
    name="Обновить меню",
)
def update_menu(id: UUID4,
                data: schemas.MenuUpdate,
                background_tasks: BackgroundTasks,
                menu: MenuService = Depends(),) -> Menu:
    try:
        menu.get(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu.update(id, data, background_tasks)


@router.delete(
    "/{id}/",
    name="Удалить меню",
)
async def delete_menu(id: UUID4,
                      background_tasks: BackgroundTasks,
                      menu: MenuService = Depends(),) -> JSONResponse:
    await menu.delete(id, background_tasks)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "Menu has been deleted"}
    )


@router.get(
        "/{id}/count",
        name="Посчитать подменю и блюда")
async def get_menu_counts(id: UUID4,
                          background_tasks: BackgroundTasks,
                          menu: MenuService = Depends()):
    return await menu.get_complex_query(id, background_tasks)

    # menu, submenu_count, dishes_count = menus
    # menu_dict = {
    #     "id": id,
    #     "title": menu.title,
    #     "description": menu.description,
    #     "submenus_count": submenu_count,
    #     "dishes_count": dishes_count,
    # }

    # return menu_dict
