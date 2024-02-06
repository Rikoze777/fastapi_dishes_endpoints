from typing import Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Dishes, Submenu
from app.repository.exceptions import SubmenuExistsException
from app.schemas.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuRepositary:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_submenu(self,
                    menu_id: UUID4,
                    submenu_id: UUID4) -> dict[Submenu, Any]:
        """
        Get a submenu by menu_id and submenu_id and return its details along with the count of dishes.

        Args:
            menu_id (UUID4): The ID of the menu.
            submenu_id (UUID4): The ID of the submenu.

        Returns:
            dict: Details of the submenu along with the count of dishes.
        """
        submenu = self.session.query(Submenu)\
                              .filter(Submenu.menu_id == menu_id)\
                              .filter(Submenu.id == submenu_id).first()
        if not submenu:
            raise SubmenuExistsException()
        result = jsonable_encoder(submenu)
        dishes = self.session.query(Dishes)\
                             .filter(Dishes.submenu_id == submenu_id).all()
        if not dishes:
            result['dishes_count'] = 0
        else:
            result['dishes_count'] = len(dishes)
        return result

    def get_submenu_list(self, id: UUID4) -> list[dict[Submenu, Any]]:
        """
        Get a list of submenu items for the given menu ID.

        :param id: UUID4 - The ID of the menu for which to retrieve submenu items.
        :return: list - A list of submenu items associated with the given menu ID.
        """
        all_submenu = self.session.query(Submenu)\
            .filter(Submenu.menu_id == id).all()
        if not all_submenu:
            return []
        else:
            list_submenu = [self.get_submenu(submenu.menu_id, submenu.id)
                            for submenu in all_submenu]
            return list_submenu

    def create_submenu(self,
                       menu_id: UUID4,
                       submenu: SubmenuCreate) -> Submenu:
        """
        Creates a new submenu for a given menu ID and submenu data.

        :param menu_id: The UUID of the menu to which the submenu belongs.
        :type menu_id: UUID4
        :param submenu: The data for the new submenu.
        :type submenu: SubmenuCreate
        :return: The newly created submenu.
        :rtype: Submenu
        """
        new_submenu = Submenu(**submenu.model_dump())
        new_submenu.dishes_count = 0
        new_submenu.menu_id = menu_id
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        return new_submenu

    def update_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4,
                       update_submenu: SubmenuUpdate) -> Submenu:
        """
        Update a submenu in the database.

        Args:
            menu_id (UUID4): The ID of the menu to which the submenu belongs.
            submenu_id (UUID4): The ID of the submenu to update.
            update_submenu (SubmenuUpdate): The updated information for the submenu.

        Returns:
            Submenu: The updated submenu object.
        """
        db_submenu = self.session.query(Submenu)\
                                 .filter(Submenu.menu_id == menu_id)\
                                 .filter(Submenu.id == submenu_id).first()
        if not db_submenu:
            raise SubmenuExistsException()
        else:
            db_submenu.title = update_submenu.title
            db_submenu.description = update_submenu.description
            self.session.add(db_submenu)
            self.session.commit()
            self.session.refresh(db_submenu)
        return db_submenu

    def delete_submenu(self,
                       menu_id: UUID4,
                       submenu_id: UUID4) -> None:
        """
        Delete a submenu from the database.

        Args:
            menu_id (UUID4): The ID of the menu containing the submenu.
            submenu_id (UUID4): The ID of the submenu to be deleted.

        Returns:
            None
        """
        db_submenu = self.session.query(Submenu)\
                                 .filter(Submenu.menu_id == menu_id)\
                                 .filter(Submenu.id == submenu_id)\
                                 .first()
        self.session.delete(db_submenu)
        self.session.commit()
