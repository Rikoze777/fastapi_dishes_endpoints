from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.repository.exceptions import SubmenuExistsException
from app.schemas import schemas
from app.services.submenu import SubmenuService

router = APIRouter(
    tags=['submenu'],
    prefix='/api/v1/menus',
)


@router.get(
    '/{menu_id}/submenus',
    response_model=list[schemas.Submenu],
    name='Просмотр списка подменю',
)
def get_submenu_list(menu_id: UUID4,
                     submenu: SubmenuService = Depends()) -> list[schemas.Submenu]:
    """
    Retrieve a list of submenus for a specific menu ID.

    Args:
        menu_id (UUID4): The unique identifier for the menu.
        submenu (SubmenuService, optional): An instance of the SubmenuService class. Defaults to None.

    Returns:
        list[schemas.Submenu]: A list of submenus associated with the specified menu ID.
    """

    return submenu.get_submenu_list(menu_id)


@router.post(
    '/{menu_id}/submenus',
    response_model=schemas.Submenu,
    name='Создать подменю',
    status_code=201,
)
def add_submenu(menu_id: UUID4,
                data: schemas.SubmenuCreate,
                submenu: SubmenuService = Depends()) -> schemas.Submenu:
    """
    A function to add a submenu to a menu, taking the menu ID, submenu data, and submenu service as parameters, and returning the created submenu.
    """
    result = submenu.create_submenu(menu_id, data)
    return result


@router.get(
    '/{menu_id}/submenus/{submenu_id}/',
    response_model=schemas.Submenu,
    name='Просмотр подменю по id',
)
def get_submenu(menu_id: UUID4,
                submenu_id: UUID4,
                submenu: SubmenuService = Depends()) -> schemas.Submenu:
    """
    A function to get a submenu by menu_id and submenu_id, using SubmenuService dependency.

    Args:
        menu_id (UUID4): The UUID of the menu.
        submenu_id (UUID4): The UUID of the submenu.
        submenu (SubmenuService, optional): The SubmenuService dependency. Defaults to Depends().

    Returns:
        schemas.Submenu: The retrieved submenu.

    Raises:
        HTTPException: If the submenu is not found, it raises an HTTPException with status code 404.
    """
    try:
        result = submenu.get_submenu(menu_id, submenu_id)
    except SubmenuExistsException:
        raise HTTPException(status_code=404, detail='submenu not found')
    return result


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/',
    response_model=schemas.Submenu,
    name='Обновить подменю',
)
def update_submenu(menu_id: UUID4,
                   submenu_id: UUID4,
                   data: schemas.SubmenuUpdate,
                   submenu: SubmenuService = Depends()) -> schemas.Submenu:
    """
    A function to update a submenu, taking in menu_id, submenu_id, data, and submenu service, and returning the updated submenu.
    """
    try:
        submenu.get_submenu(menu_id, submenu_id)
    except SubmenuExistsException:
        raise HTTPException(status_code=404, detail='submenu not found')
    update_submenu = submenu.update_submenu(menu_id, submenu_id, data)
    return update_submenu


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/',
    name='Удаление подменю',
)
def delete_submenu(menu_id: UUID4,
                   submenu_id: UUID4,
                   submenu: SubmenuService = Depends()):
    """
    A view function to delete a submenu.

    Args:
        menu_id (UUID4): The ID of the menu.
        submenu_id (UUID4): The ID of the submenu to be deleted.
        submenu (SubmenuService, optional): An instance of SubmenuService. Defaults to Depends().

    Returns:
        JSONResponse: A JSON response indicating the status of the deletion operation.
    """
    submenu.delete_submenu(menu_id, submenu_id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'Submenu has been deleted'}
    )
