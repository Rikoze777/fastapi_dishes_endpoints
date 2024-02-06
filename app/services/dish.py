import json

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4

from app.database.db import get_redis
from app.repository.dishes_repo import DishesRepository
from app.schemas import schemas


class DishesService:
    def __init__(self,
                 repository: DishesRepository = Depends()) -> None:
        self.repository = repository
        self.cache = get_redis()

    def get_dish(self,
                 submenu_id: UUID4,
                 dish_id: UUID4) -> schemas.Dishes:
        """
        Retrieves a dish from the cache or the repository, updates its price format, and caches it for future use.

        :param submenu_id: The UUID of the submenu to which the dish belongs.
        :param dish_id: The UUID of the dish to retrieve.
        :return: A schemas.Dishes object representing the retrieved dish.
        """
        key = str(dish_id)
        dish = self.cache.get(key)
        if not dish:
            dishh = self.repository.get_dish(submenu_id, dish_id)
            dishh.price = f'{float(dishh.price):.2f}'
            dishh = jsonable_encoder(dishh)
            self.cache.set(key, json.dumps(dishh))
            self.cache.expire(key, 300)
            return dishh
        else:
            return json.loads(dish.decode('utf-8'))

    def get_dishes_list(self,
                        submenu_id: UUID4) -> list[schemas.Dishes]:
        """
        Get a list of dishes for a given submenu ID.

        Args:
            submenu_id (UUID4): The ID of the submenu for which to retrieve the dishes.

        Returns:
            list: A list of dishes for the given submenu ID.
        """
        dishes = self.cache.get('dishes')
        if not dishes:
            dishes = self.repository.get_dishes_list(submenu_id)
            for dish in dishes:
                dish.price = f'{float(dish.price):.2f}'
            dishes = jsonable_encoder(dishes)
            self.cache.set('dishes', json.dumps(dishes))
            self.cache.expire('dishes', 300)
            return dishes
        else:
            return json.loads(dishes.decode('utf-8'))

    def create_dish(self,
                    submenu_id: UUID4,
                    dish: schemas.DishesCreate) -> schemas.Dishes:
        """
        Create a dish for the given submenu ID using the provided dish details.

        Args:
            submenu_id (UUID4): The ID of the submenu for which the dish is being created.
            dish (schemas.DishesCreate): The details of the dish being created.

        Returns:
            schemas.Dishes: The created dish.
        """
        result = self.repository.create_dish(submenu_id, dish)
        self.cache.delete('menu', 'submenu', 'dishes')
        dish_get = self.repository.get_dish(submenu_id, result.id)
        dish_get.price = f'{float(dish_get.price):.2f}'
        return dish_get

    def update_dish(self,
                    submenu_id: UUID4,
                    dish_id: UUID4,
                    update_dish: schemas.DishesUpdate) -> schemas.Dishes:
        """
        Update a dish for a given submenu, based on the provided dish ID and update information.

        Args:
            submenu_id (UUID4): The ID of the submenu to which the dish belongs.
            dish_id (UUID4): The ID of the dish to be updated.
            update_dish (schemas.DishesUpdate): The updated information for the dish.

        Returns:
            schemas.Dishes: The updated dish.
        """
        result = self.repository.update_dish(submenu_id, dish_id, update_dish)
        self.cache.delete(str(dish_id))
        self.cache.delete('dishes')
        dish_get = self.repository.get_dish(submenu_id, result.id)
        dish_get.price = f'{float(dish_get.price):.2f}'
        return dish_get

    def delete_dish(self, submenu_id: UUID4, dish_id: UUID4) -> None:
        """
        Deletes a dish from the submenu and updates the cache accordingly.

        :param submenu_id: The UUID of the submenu from which the dish will be deleted.
        :type submenu_id: UUID4
        :param dish_id: The UUID of the dish to be deleted.
        :type dish_id: UUID4
        """
        self.repository.delete_dish(submenu_id, dish_id)
        self.cache.delete(str(dish_id))
        self.cache.delete('menu', 'submenu', 'dishes')
