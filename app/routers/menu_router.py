from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.database.models import Menu
from app.repository.exceptions import MenuExistsException
from app.schemas import schemas
from app.services.menu import MenuService

router = APIRouter(
    tags=["menu"],
    prefix="/api/v1/menus",
)


@router.get(
    "/",
    response_model=list[schemas.Menu],
    responses={404: {"model": schemas.NotFoundError}},
    name="Список меню",
)
async def get_menu_list(menu: MenuService = Depends()) -> list[schemas.Menu]:
    return await menu.get_menu_list()


@router.post(
    "/",
    response_model=schemas.Menu,
    name="Создать меню",
    status_code=status.HTTP_201_CREATED,
)
async def add_menu(
    data: schemas.MenuCreate,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
) -> dict[Menu, Any]:
    return await menu.create(data, background_tasks)


@router.get(
    "/{id}/",
    response_model=schemas.MenuExtended,
    responses={404: {"model": schemas.NotFoundError}},
    name="Меню по id",
)
async def get_menu(id: UUID4, menu: MenuService = Depends()) -> dict[Menu, Any]:
    try:
        return_menu = await menu.get_complex_query(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail="menu not found")
    return return_menu


@router.patch(
    "/{id}/",
    response_model=schemas.Menu,
    responses={404: {"model": schemas.NotFoundError}},
    name="Обновить меню",
)
async def update_menu(
    id: UUID4,
    data: schemas.MenuUpdate,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
) -> dict[Menu, Any]:
    try:
        up_menu = await menu.update(id, data, background_tasks)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail="menu not found")
    return up_menu


@router.delete(
    "/{id}/",
    responses={404: {"model": schemas.NotFoundError}},
    name="Удалить меню",
)
async def delete_menu(
    id: UUID4, background_tasks: BackgroundTasks, menu: MenuService = Depends()
) -> JSONResponse:
    await menu.delete(id, background_tasks)
    return JSONResponse(
        status_code=200, content={"status": "true", "message": "Menu has been deleted"}
    )


@router.get(
    "/{id}/count",
    responses={404: {"model": schemas.NotFoundError}},
    name="Посчитать подменю и блюда",
)
async def get_menu_counts(id: UUID4, menu: MenuService = Depends()) -> dict[str, Any]:
    return await menu.get_complex_query(id)
