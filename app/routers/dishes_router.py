from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
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
    responses={404: {'model': schemas.NotFoundError}},
    name='Список блюд',
)
async def get_dishes_list(
    menu_id: UUID4, submenu_id: UUID4, dishes: DishesService = Depends()
) -> list[schemas.Dishes]:
    dishes_list = await dishes.get_dishes_list(menu_id, submenu_id)

    return dishes_list


@router.get(
    '/dishes/{dish_id}',
    response_model=schemas.Dishes,
    responses={404: {'model': schemas.NotFoundError}},
    name='Блюдо по id',
)
async def get_dish(
    menu_id: UUID4, submenu_id: UUID4, dish_id: UUID4, dishes: DishesService = Depends()
) -> schemas.Dishes:
    try:
        dish = await dishes.get(menu_id, submenu_id, dish_id)
    except DishExistsException:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish


@router.post(
    '/dishes',
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=status.HTTP_201_CREATED,
)
async def add_dish(
    menu_id: UUID4,
    submenu_id: UUID4,
    data: schemas.DishesCreate,
    background_tasks: BackgroundTasks,
    dishes: DishesService = Depends(),
) -> schemas.Dishes:
    dish = await dishes.create(menu_id, submenu_id, data, background_tasks)
    dish.price = f'{float(dish.price):.2f}'
    return dish


@router.patch(
    '/dishes/{dish_id}',
    response_model=schemas.Dishes,
    responses={404: {'model': schemas.NotFoundError}},
    name='Обновить блюдо',
)
async def update_dish(
    menu_id: UUID4,
    submenu_id: UUID4,
    dish_id: UUID4,
    data: schemas.DishesUpdate,
    background_tasks: BackgroundTasks,
    dishes: DishesService = Depends(),
) -> schemas.Dishes:
    try:
        updated_dish = await dishes.update(
            menu_id, submenu_id, dish_id, data, background_tasks
        )
    except DishExistsException:
        raise HTTPException(status_code=404, detail='dish not found')
    return updated_dish


@router.delete(
    '/dishes/{dish_id}',
    responses={404: {'model': schemas.NotFoundError}},
    name='Удалить блюдо',
)
async def delete_dish(
    menu_id: UUID4,
    submenu_id: UUID4,
    dish_id: UUID4,
    background_tasks: BackgroundTasks,
    dishes: DishesService = Depends(),
) -> JSONResponse:
    await dishes.delete(menu_id, submenu_id, dish_id, background_tasks)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'The dish has been deleted'},
    )
