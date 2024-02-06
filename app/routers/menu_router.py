from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
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
    response_model=list[schemas.Menu],
    responses={404: {'model': schemas.NotFoundError}},
    name='Список меню',
)
def get_menu_list(menu: MenuService = Depends()) -> list[schemas.Menu]:
    """
    A function to retrieve a list of menus using the MenuService dependency.
    """
    return menu.get_menu_list()


@router.post(
    '/',
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=status.HTTP_201_CREATED,
)
def add_menu(data: schemas.MenuCreate,
             menu: MenuService = Depends()) -> dict[Menu, Any]:
    """
    A function to add a menu using the provided data and MenuService instance.

    Args:
        data (schemas.MenuCreate): The data for creating the menu.
        menu (MenuService, optional): An instance of MenuService. Defaults to Depends().

    Returns:
        The created menu.
    """
    return menu.create_menu(data)


@router.get(
    '/{id}/',
    response_model=schemas.Menu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Меню по id',
)
def get_menu(id: UUID4,
             menu: MenuService = Depends()) -> dict[Menu, Any]:
    """
    A function to get the menu by its ID using MenuService dependency.

    Args:
        id (UUID4): The ID of the menu.
        menu (MenuService, optional): The MenuService dependency. Defaults to Depends().

    Returns:
        schemas.Menu: The menu object.

    Raises:
        HTTPException: If the menu is not found.
    """
    try:
        return_menu = menu.get_menu(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail='menu not found')
    return return_menu


@router.patch(
    '/{id}/',
    response_model=schemas.Menu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Обновить меню',
)
def update_menu(id: UUID4,
                data: schemas.MenuUpdate,
                menu: MenuService = Depends()) -> dict[Menu, Any]:
    """
    Update a menu with the given ID using the provided data.

    Parameters:
        id (UUID4): The ID of the menu to be updated.
        data (schemas.MenuUpdate): The updated menu data.
        menu (MenuService, optional): An instance of the MenuService class. Defaults to None.

    Returns:
        schemas.Menu: The updated menu.

    Raises:
        HTTPException: If the menu with the given ID is not found.
    """
    try:
        up_menu = menu.update_menu(id, data)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail='menu not found')
    return up_menu


@router.delete(
    '/{id}/',
    responses={404: {'model': schemas.NotFoundError}},
    name='Удалить меню',
)
def delete_menu(id: UUID4,
                menu: MenuService = Depends()) -> JSONResponse:
    """
    Delete a menu by its ID.

    Args:
        id (UUID4): The ID of the menu to be deleted.
        menu (MenuService, optional): An instance of the MenuService. Defaults to Depends().

    Returns:
        JSONResponse: The JSON response indicating the status of the deletion.
    """
    menu.delete_menu(id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'Menu has been deleted'}
    )


@router.get(
    '/{id}/count',
    responses={404: {'model': schemas.NotFoundError}},
    name='Посчитать подменю и блюда')
def get_menu_counts(id: UUID4,
                    menu: MenuService = Depends()) -> dict[str, Any]:
    """
    A function to retrieve menu counts based on the provided ID and menu service.

    Parameters:
        id: UUID4 - The ID used to retrieve the menu counts.
        menu: MenuService - An instance of the MenuService class used to retrieve menu counts.

    Returns:
        dict - A dictionary containing the menu counts based on the provided ID.
    """
    return menu.get_complex_query(id)
