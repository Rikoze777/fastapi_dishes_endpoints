from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.repository.exceptions import DishExistsException
from app.schemas import schemas
from app.services.dish import DishesService

router = APIRouter(
    tags=['dishes'],
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
)


@router.get(
    '/dishes',
    response_model=list[schemas.Dishes],
    name='Список блюд',
)
def get_dishes_list(submenu_id: UUID4,
                    dishes: DishesService = Depends()) -> list[schemas.Dishes]:
    return dishes.get_dishes_list(submenu_id)


@router.get(
    '/dishes/{id}',
    response_model=schemas.Dishes,
    name='Блюдо по id',
)
def get_dish(submenu_id: UUID4,
             dish_id: UUID4,
             dishes: DishesService = Depends()) -> schemas.Dishes:
    try:
        dish = dishes.get_dish(submenu_id, dish_id)
    except DishExistsException:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.post(
    '/dishes',
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=201,
)
def add_dish(submenu_id: UUID4,
             data: schemas.DishesCreate,
             dishes: DishesService = Depends()) -> schemas.Dishes:
    return dishes.create_dish(submenu_id, data)


@router.patch(
    '/dishes/{id}',
    response_model=schemas.Dishes,
    name='Обновить блюдо',
)
def update_dish(submenu_id: UUID4,
                dish_id: UUID4,
                data: schemas.DishesUpdate,
                dishes: DishesService = Depends()) -> schemas.Dishes:
    try:
        updated_dish = dishes.update_dish(submenu_id, dish_id, data)
    except DishExistsException:
        raise HTTPException(status_code=404, detail='dish not found')
    return updated_dish


@router.delete(
    '/dishes/{id}',
    name='Удалить блюдо',
)
def delete_dish(submenu_id: UUID4,
                dishes_id: UUID4,
                dishes: DishesService = Depends()):
    dishes.delete_dish(submenu_id, dishes_id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'The dish has been deleted'}
    )
