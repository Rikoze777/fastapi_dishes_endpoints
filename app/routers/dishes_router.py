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
    """
    A function to get a list of dishes based on the submenu ID.

    Parameters:
        submenu_id (UUID4): The ID of the submenu for which the list of dishes is requested.
        dishes (DishesService, optional): An instance of DishesService, defaults to None.

    Returns:
        list[schemas.Dishes]: A list of dishes based on the provided submenu ID.
    """
    return dishes.get_dishes_list(submenu_id)


@router.get(
    '/dishes/{id}',
    response_model=schemas.Dishes,
    name='Блюдо по id',
)
def get_dish(submenu_id: UUID4,
             dish_id: UUID4,
             dishes: DishesService = Depends()) -> schemas.Dishes:
    """
    A function to retrieve a dish by its submenu ID and dish ID using the DishesService.

    Args:
        submenu_id (UUID4): The ID of the submenu.
        dish_id (UUID4): The ID of the dish.
        dishes (DishesService, optional): An instance of DishesService. Defaults to Depends().

    Returns:
        schemas.Dishes: The retrieved dish.
    """
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
    """
    A function to add a dish to the submenu.

    Args:
        submenu_id (UUID4): The ID of the submenu to add the dish to.
        data (DishesCreate): The data for creating the dish.
        dishes (DishesService, optional): An instance of DishesService. Defaults to None.

    Returns:
        schemas.Dishes: The created dish.
    """
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
    """
    A function to update a dish with the given submenu ID, dish ID, and data, using the DishesService.
    It returns the updated dish as per the schemas.Dishes type.
    """
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
    """
    A function to delete a dish from the database.

    Args:
        submenu_id (UUID4): The ID of the submenu to which the dish belongs.
        dishes_id (UUID4): The ID of the dish to be deleted.
        dishes (DishesService, optional): An instance of the DishesService class. Defaults to Depends().

    Returns:
        JSONResponse: The response indicating the status of the deletion operation.
    """
    dishes.delete_dish(submenu_id, dishes_id)
    return JSONResponse(
        status_code=200,
        content={'status': 'true', 'message': 'The dish has been deleted'}
    )
