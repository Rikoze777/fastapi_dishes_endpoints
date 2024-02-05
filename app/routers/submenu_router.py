from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.crud.exceptions import SubmenuExistsException
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
                     submenu: SubmenuService = Depends())\
        -> list[schemas.Submenu]:
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
    submenu.delete_submenu(menu_id, submenu_id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'Submenu has been deleted'}
    )
