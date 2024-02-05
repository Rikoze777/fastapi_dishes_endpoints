import json

from fastapi import Depends
from pydantic import UUID4

from app.crud.dishes_crud import DishesRepository
from app.database.db import get_redis
from app.schemas import schemas


class DishesService:
    def __init__(self,
                 repository: DishesRepository = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_dish(self,
                 submenu_id: UUID4,
                 dish_id: UUID4) -> schemas.Dishes:
        if not self.cache.get(str(dish_id)):
            dish = self.repository.get_dish(submenu_id, dish_id)
            dish.price = f'{float(dish.price):.2f}'
            self.cache.set(id, json.dumps(dish))
            self.cache.expire(submenu_id, 300)
            return dish
        else:
            return json.loads(self.cache.get(str(dish_id)))

    def get_dishes_list(self,
                        submenu_id: UUID4) -> list:
        if not self.cache.get('dishes'):
            dishes = self.repository.get_dishes_list(submenu_id)
            for dish in dishes:
                dish.price = f'{float(dish.price):.2f}'
            self.cache.set('dishes', json.dumps(dishes))
            self.cache.expire('dishes', 300)
            return dishes
        else:
            return json.loads(self.cache.get('dishes'))

    def create_dish(self,
                    submenu_id: UUID4,
                    dish: schemas.DishesCreate) -> schemas.Dishes:
        result = self.repository.create_dish(submenu_id, dish)
        result.price = str(f'{float(result.price):.2f}')
        self.cache.delete('menu', 'submenu', 'dishes')
        return result

    def update_dish(self,
                    submenu_id: UUID4,
                    dish_id: UUID4,
                    update_dish: schemas.DishesUpdate) -> schemas.Dishes:
        result = self.repository.update_dish(submenu_id, dish_id, update_dish)
        result.price = str(f'{float(result.price):.2f}')
        self.cache.delete(str(dish_id))
        self.cache.delete('dishes')
        return result

    def delete_dish(self, submenu_id: UUID4, dish_id: UUID4):
        self.repository.delete_dish(submenu_id, dish_id)
        self.cache.delete(str(dish_id))
        self.cache.delete('menu', 'submenu', 'dishes')
