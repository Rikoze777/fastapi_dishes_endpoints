from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.database.models import Submenu
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
    responses={404: {'model': schemas.NotFoundError}},
    name='Просмотр списка подменю',
)
async def get_submenu_list(
    menu_id: UUID4, submenu: SubmenuService = Depends()
) -> list[Submenu]:
    """
    Asynchronously retrieves a list of submenus for the given menu_id.

    Args:
        menu_id (UUID4): The ID of the menu for which the submenus are being retrieved.
        submenu (SubmenuService): An instance of SubmenuService obtained from the dependency injection system.

    Returns:
        list[Submenu]: A list of submenus associated with the given menu_id.
    """
    return await submenu.get_submenu_list(menu_id)


@router.post(
    '/{menu_id}/submenus',
    response_model=schemas.Submenu,
    name='Создать подменю',
    status_code=status.HTTP_201_CREATED,
)
async def add_submenu(
    menu_id: UUID4,
    data: schemas.SubmenuCreate,
    background_tasks: BackgroundTasks,
    submenu: SubmenuService = Depends(),
) -> dict[Submenu, Any]:
    """
    Async function to add a submenu to a menu.

    Args:
        menu_id (UUID4): The ID of the menu to which the submenu will be added.
        data (SubmenuCreate): The data for creating the submenu.
        background_tasks (BackgroundTasks): Background tasks to be run.
        submenu (SubmenuService, optional): The service for interacting with submenus. Defaults to None.

    Returns:
        dict[Submenu, Any]: The created submenu.
    """
    return await submenu.create(menu_id, data, background_tasks)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/',
    response_model=schemas.Submenu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Просмотр подменю по id',
)
async def get_submenu(
    menu_id: UUID4, submenu_id: UUID4, submenu: SubmenuService = Depends()
) -> dict[Submenu, Any]:
    """
    A function to get a submenu by menu_id and submenu_id using SubmenuService dependency.
    Parameters:
        - menu_id: UUID4
        - submenu_id: UUID4
        - submenu: SubmenuService
    Returns:
        - dict[Submenu, Any]
    """
    try:
        result = await submenu.get(menu_id, submenu_id)
    except SubmenuExistsException:
        raise HTTPException(status_code=404, detail='submenu not found')
    return result


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/',
    response_model=schemas.Submenu,
    responses={404: {'model': schemas.NotFoundError}},
    name='Обновить подменю',
)
async def update_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    data: schemas.SubmenuUpdate,
    background_tasks: BackgroundTasks,
    submenu: SubmenuService = Depends(),
) -> type[Submenu]:
    """
    A function to update a submenu with the specified menu_id, submenu_id, and data using BackgroundTasks, and return the updated submenu.

    Parameters:
        menu_id: UUID4 - The ID of the menu
        submenu_id: UUID4 - The ID of the submenu to be updated
        data: schemas.SubmenuUpdate - The data to update the submenu
        background_tasks: BackgroundTasks - Background tasks to be used
        submenu: SubmenuService - The service for managing submenus

    Returns:
        type[Submenu]: The updated submenu
    """
    try:
        await submenu.get(menu_id, submenu_id)
    except SubmenuExistsException:
        raise HTTPException(status_code=404, detail='submenu not found')
    update_submenu = await submenu.update(menu_id, submenu_id, data, background_tasks)
    return update_submenu


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/',
    responses={404: {'model': schemas.NotFoundError}},
    name='Удаление подменю',
)
async def delete_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    background_tasks: BackgroundTasks,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    """
    A function to delete a submenu with the given menu_id and submenu_id.
    It takes in the menu_id, submenu_id, background_tasks, and submenu as parameters.
    It returns a JSONResponse with a status code of 200 and content indicating the status of the deletion.
    """

    await submenu.delete(menu_id, submenu_id, background_tasks)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'Submenu has been deleted'},
    )
