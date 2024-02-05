from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.crud.exceptions import SubmenuExistsException
from app.database.db import get_db
from app.database.models import Dishes, Submenu
from app.schemas.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuRepositary:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_submenu(self,
                    menu_id: UUID4,
                    submenu_id: UUID4):
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

    def get_submenu_list(self, id: UUID4):
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
                       submenu: SubmenuCreate):
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
                       update_submenu: SubmenuUpdate):
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
                       submenu_id: UUID4):
        db_submenu = self.session.query(Submenu)\
                                 .filter(Submenu.menu_id == menu_id)\
                                 .filter(Submenu.id == submenu_id)\
                                 .first()
        self.session.delete(db_submenu)
        self.session.commit()
