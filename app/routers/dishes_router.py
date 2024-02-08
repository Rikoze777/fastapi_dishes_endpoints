from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from typing import List
from app.schemas import schemas
from fastapi.responses import JSONResponse
from pydantic import UUID4
from app.services.dish_service import DishService


router = APIRouter(
    tags=["dishes"],
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}",
)


@router.get(
    "/dishes",
    response_model=List[schemas.Dishes],
    name="Список блюд",
)
async def get_dishes_list(menu_id: UUID4,
                          submenu_id: UUID4,
                          service: DishService = Depends()):
    dishes_list = await service.get_dishes_list(menu_id, submenu_id)
    for dish in dishes_list:
        dish.price = "{:.2f}".format(float(dish.price))
    return dishes_list


@router.get(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Блюдо по id",
)
async def get_dish(menu_id: UUID4,
                   submenu_id: UUID4,
                   id: UUID4,
                   service: DishService = Depends()):
    try:
        dish = await service.get(menu_id, submenu_id, id)
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    dish.price = "{:.2f}".format(float(dish.price))
    return dish


@router.post(
    "/dishes",
    response_model=schemas.Dishes,
    name='Создать блюдо',
    status_code=201,
)
async def add_dish(menu_id: UUID4,
                   submenu_id: UUID4,
                   data: schemas.DishesCreate,
                   background_tasks: BackgroundTasks,
                   service: DishService = Depends()):
    dish = await service.create(menu_id, submenu_id, data, background_tasks)
    dish.price = str("{:.2f}".format(float(dish.price)))
    return dish


@router.patch(
    "/dishes/{id}",
    response_model=schemas.Dishes,
    name="Обновить блюдо",
)
async def update_dish(menu_id: UUID4,
                      submenu_id: UUID4,
                      id: UUID4,
                      data: schemas.DishesUpdate,
                      background_tasks: BackgroundTasks,
                      service: DishService = Depends()):
    try:
        updated_dish = await service.update(menu_id, submenu_id, id, data, background_tasks)
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    updated_dish.price = str("{:.2f}".format(float(updated_dish.price)))
    return updated_dish


@router.delete(
    "/dishes/{id}",
    name="Удалить блюдо",
)
async def delete_dish(menu_id: UUID4,
                      submenu_id: UUID4,
                      id: UUID4,
                      background_tasks: BackgroundTasks,
                      service: DishService = Depends()):
    await service.delete(menu_id, submenu_id, id, background_tasks)
    return JSONResponse(
        status_code=200,
        content={"status": "true", "message": "The dish has been deleted"}
    )
