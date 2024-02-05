from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Dishes
from app.repository.exceptions import DishExistsException
from app.schemas.schemas import DishesCreate, DishesUpdate


class DishesRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_dish(self, submenu_id: UUID4, id: UUID4):
        """
        Retrieves a dish from the database based on the provided submenu_id and id.

        Args:
            submenu_id (UUID4): The UUID of the submenu to which the dish belongs.
            id (UUID4): The UUID of the dish.

        Returns:
            Dishes: The dish object from the database.

        Raises:
            DishExistsException: If the dish does not exist in the database.
        """
        dish = self.session.query(Dishes)\
                           .filter(Dishes.submenu_id == submenu_id)\
                           .filter(Dishes.id == id).first()
        if not dish:
            raise DishExistsException()
        return dish

    def create_dish(self, submenu_id: UUID4, dish: DishesCreate):
        """
        Create a new dish for a given submenu and add it to the database.

        :param submenu_id: The UUID of the submenu to which the dish belongs
        :type submenu_id: UUID4
        :param dish: The details of the dish to be created
        :type dish: DishesCreate
        :return: The newly created dish
        :rtype: Dishes
        """
        new_dish = Dishes(**dish.model_dump())
        new_dish.submenu_id = submenu_id
        new_dish.price = new_dish.price
        self.session.add(new_dish)
        self.session.commit()
        return new_dish

    def update_dish(self,
                    submenu_id: UUID4,
                    dish_id: UUID4,
                    update_dish: DishesUpdate):
        """
        Updates a dish in the submenu with the given submenu_id and dish_id using the provided DishesUpdate object.

        Args:
            submenu_id (UUID4): The UUID of the submenu containing the dish to be updated.
            dish_id (UUID4): The UUID of the dish to be updated.
            update_dish (DishesUpdate): The object containing the updated title, description, and price for the dish.

        Returns:
            db_dish: The updated dish object.
        """
        db_dish = self.get_dish(submenu_id, dish_id)
        if not db_dish:
            raise DishExistsException()
        else:
            db_dish.title = update_dish.title
            db_dish.description = update_dish.description
            db_dish.price = update_dish.price
            self.session.add(db_dish)
            self.session.commit()
            self.session.refresh(db_dish)
        return db_dish

    def get_dishes_list(self, submenu_id: UUID4):
        """
        Retrieves a list of dishes based on the provided submenu ID.

        Args:
            submenu_id (UUID4): The ID of the submenu.

        Returns:
            list: A list of dishes corresponding to the submenu ID.
        """
        all_dishes = self.session.query(Dishes)\
                                 .filter(Dishes.submenu_id == submenu_id)\
                                 .all()
        if not all_dishes:
            return []
        else:
            list_dishes = [self.get_dish(submenu_id, dish.id)
                           for dish in all_dishes]
            return list_dishes

    def delete_dish(self, submenu_id: UUID4, id: UUID4):
        """
        Deletes a dish from the database.

        Args:
            submenu_id (UUID4): The ID of the submenu the dish belongs to.
            id (UUID4): The ID of the dish to be deleted.

        Returns:
            None
        """
        db_dish = self.session.query(Dishes)\
                              .filter(Dishes.submenu_id == submenu_id)\
                              .filter(Dishes.id == id).first()
        self.session.delete(db_dish)
        self.session.commit()
