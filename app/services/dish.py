import json
from typing import List
from fastapi import Depends
from pydantic import UUID4
from app.crud.dishes_crud import DishesRepositary
from app.database.db import get_redis
from app.schemas import schemas


class DishesService:
    def __init__(self,
                 repository: DishesRepositary = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_dish(self,
                 submenu_id: UUID4,
                 dish_id: UUID4) -> schemas.Dishes:
        dish = self.repository.get_dish(submenu_id, dish_id)
        dish.price = "{:.2f}".format(float(dish.price))
        return dish

    def get_dishes_list(self,
                        submenu_id: UUID4) -> List[schemas.Dishes]:
        dishes = self.repository.get_dishes_list(submenu_id)
        for dish in dishes:
            dish.price = "{:.2f}".format(float(dish.price))
        return dishes

    def create_dish(self,
                    submenu_id: UUID4,
                    dish: schemas.DishesCreate) -> schemas.Dishes:
        result = self.repository.create_dish(submenu_id, dish)
        # updated_dish = self.repository.get_dish(submenu_id, result.id)
        result.price = str("{:.2f}".format(float(result.price)))
        return result

    def update_dish(self,
                    submenu_id: UUID4,
                    dish_id: UUID4,
                    update_dish: schemas.DishesUpdate) -> schemas.Dishes:
        result = self.repository.update_dish(submenu_id, dish_id, update_dish)
        result.price = str("{:.2f}".format(float(result.price)))
        return result

    def delete_dish(self, submenu_id: UUID4, id: UUID4):
        self.repository.delete_dish(submenu_id, id)
