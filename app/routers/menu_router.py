from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.database.models import Menu
from app.repository.exceptions import MenuExistsException
from app.schemas import schemas
from app.services.menu import MenuService

router = APIRouter(
    tags=['menu'],
    prefix='/api/v1/menus',
)


@router.get(
    '/',
    response_model=list[schemas.MenuItem],
    responses={404: {'model': schemas.NotFoundError}},
    name='Список меню',
)
async def get_menu_list(menu: MenuService = Depends()) -> list[schemas.MenuItem]:
    """
    A function to get the menu list using MenuService dependency and returning a list of MenuItem schemas.
    """
    list = await menu.get_menu_list()
    return list


@router.post(
    '/',
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=status.HTTP_201_CREATED,
)
async def add_menu(
    data: schemas.MenuCreate,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
) -> dict[schemas.Menu, Any]:
    """
    Create a menu.

    Args:
        data (schemas.MenuCreate): The menu data to be created.
        background_tasks (BackgroundTasks): The background tasks to be executed.
        menu (MenuService, optional): The menu service. Defaults to Depends().

    Returns:
        dict[schemas.Menu, Any]: The created menu.
    """
    return await menu.create(data, background_tasks)


@router.get(
    '/{id}/',
    response_model=schemas.Menu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Меню по id',
)
async def get_menu(id: UUID4, menu: MenuService = Depends()) -> dict[str, Any]:
    """
    A function to get a menu by its ID, with parameters id: UUID4, menu: MenuService = Depends(), and return type dict[str, Any].
    """
    try:
        return_menu = await menu.get_complex_query(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail='menu not found')
    return return_menu


@router.patch(
    '/{id}/',
    response_model=schemas.Menu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Обновить меню',
)
async def update_menu(
    id: UUID4,
    data: schemas.MenuUpdate,
    background_tasks: BackgroundTasks,
    menu: MenuService = Depends(),
) -> type[Menu]:
    """
    A function to update a menu item.

    Args:
        id (UUID4): The ID of the menu item to be updated.
        data (schemas.MenuUpdate): The updated menu data.
        background_tasks (BackgroundTasks): Background tasks to be run during the update.
        menu (MenuService, optional): An instance of MenuService. Defaults to None.

    Returns:
        type[Menu]: The updated menu item.
    """
    try:
        up_menu = await menu.update(id, data, background_tasks)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail='menu not found')
    return up_menu


@router.delete(
    '/{id}/',
    responses={404: {'model': schemas.NotFoundError}},
    name='Удалить меню',
)
async def delete_menu(
    id: UUID4, background_tasks: BackgroundTasks, menu: MenuService = Depends()
) -> JSONResponse:
    """
    Asynchronous function to delete a menu item.

    Args:
        id (UUID4): The unique identifier of the menu item to be deleted.
        background_tasks (BackgroundTasks): A helper class for running background tasks.
        menu (MenuService): An instance of the MenuService class.

    Returns:
        JSONResponse: A JSON response indicating the status of the deletion process.
    """
    await menu.delete(id, background_tasks)
    return JSONResponse(
        status_code=200, content={'status': 'true', 'message': 'Menu has been deleted'}
    )


@router.get(
    '/{id}/count',
    responses={404: {'model': schemas.NotFoundError}},
    name='Посчитать подменю и блюда',
)
async def get_menu_counts(id: UUID4, menu: MenuService = Depends()) -> dict[str, Any]:
    """
    A function to get the counts of submenus and dishes for a given menu ID.

    Args:
        id: The UUID4 ID of the menu.
        menu: An instance of the MenuService class.

    Returns:
        A dictionary with the counts of submenus and dishes for the given menu ID.
    """
    return await menu.get_complex_query(id)


@router.get(
    '/all',
    responses={404: {'model': schemas.NotFoundError}},
    name='Вывести все меню',
)
async def get_all_menus(
    menu: MenuService = Depends(),
):
    """
    A function to get all menus from the menu service.

    Parameters:
    - menu: MenuService - an instance of the MenuService class

    """
    return await menu.get_all_menus()
