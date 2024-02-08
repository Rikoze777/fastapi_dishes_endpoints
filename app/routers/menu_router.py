from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from typing import List
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.crud.exceptions import MenuExistsException

from app.services.menu_service import MenuService
from app.schemas.schemas import Menu, MenuCreate, MenuExtended, MenuUpdate


router = APIRouter(
    tags=["menu"],
    prefix="/api/v1/menus",
)


@router.get(
    "/",
    response_model=List[Menu],
    name="Список меню",
)
async def get_menu_list(menu: MenuService = Depends()) -> List[Menu]:
    return await menu.get_menu_list()


@router.post(
    "/",
    response_model=Menu,
    name='Создать меню',
    status_code=201,
)
async def add_menu(data: MenuCreate,
                   background_tasks: BackgroundTasks,
                   menu: MenuService = Depends(),) -> Menu:
    return await menu.create(data, background_tasks)


@router.get(
    "/{id}/",
    response_model=Menu,
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
    response_model=Menu,
    name="Обновить меню",
)
def update_menu(id: UUID4,
                data: MenuUpdate,
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
        response_model=MenuExtended,
        name="Посчитать подменю и блюда")
async def get_menu_counts(id: UUID4,
                          menu: MenuService = Depends()):
    menu_extended = await menu.count(id)
    return menu_extended
