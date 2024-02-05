from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.crud.exceptions import MenuExistsException
from app.schemas import schemas
from app.services.menu import MenuService

router = APIRouter(
    tags=['menu'],
    prefix='/api/v1//menus',
)


@router.get(
    '/',
    response_model=list[schemas.Menu],
    name='Список меню',
)
def get_menu_list(menu: MenuService = Depends()):
    return menu.get_menu_list()


@router.post(
    '/',
    response_model=schemas.Menu,
    name='Создать меню',
    status_code=201,
)
def add_menu(data: schemas.MenuCreate, menu: MenuService = Depends()):
    result = menu.create_menu(data)
    return menu.get_menu(result.id)


@router.get(
    '/{id}/',
    response_model=schemas.Menu,
    name='Меню по id',
)
def get_menu(id: UUID4, menu: MenuService = Depends()):
    try:
        menu = menu.get_menu(id)
    except MenuExistsException:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu


@router.patch(
    '/{id}/',
    response_model=schemas.Menu,
    name='Обновить меню',
)
def update_menu(id: UUID4,
                data: schemas.MenuUpdate,
                menu: MenuService = Depends()):
    menu.get_menu(id)
    if not menu:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu.update_menu(id, data)


@router.delete(
    '/{id}/',
    name='Удалить меню',
)
def delete_menu(id: UUID4, menu: MenuService = Depends()):
    menu.delete_menu(id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'Menu has been deleted'}
    )


@router.get(
    '/{id}/count',
    name='Посчитать подменю и блюда')
def get_menu_counts(id: UUID4, menu: MenuService = Depends()) -> dict:
    return menu.get_complex_query(id)
