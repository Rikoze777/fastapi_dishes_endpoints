from typing import List, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.database.db_exceptions import SubmenuNotFound
from app.database.models import SubMenu
from app.api.schemas import SubmenuCreate, SubmenuUpdate


class SubmenuStorage:

    def __init__(self, db: Session, submenu_id: UUID,
                 menu_id: UUID, submenu_create=SubmenuCreate,
                 submenu_update=SubmenuUpdate):
        self.db = db
        self.submenu_id = submenu_id
        self.menu_id = menu_id
        self.submenu_create = submenu_create
        self.submenu_update = submenu_update

    def get_submenu(self):
        submenu = self.db.query(SubMenu).filter(SubMenu.id == self.menu_id).filter(id == self.submenu_id).first()
        if not submenu:
            raise SubmenuNotFound()
        return submenu

    def get_submenu_list(self):
        all_submenu = self.db.query(SubMenu).filter(SubMenu.id == self.menu_id).scalar().all()
        if not all_submenu:
            return []
        return all_submenu

    def create_submenu(self) -> SubMenu:
        new_submenu = SubMenu(title=self.submenu_update.title,
                              description=self.submenu_update.description,
                              menu_id=self.menu_id)
        self.db.add(new_submenu)
        self.db.commit()
        return new_submenu

    def update_submenu(self) -> Union[SubMenu, None]:
        db_submenu = self.db.query(SubMenu).filter(SubMenu.id == self.menu_id).filter(id == self.submenu_id).scalar_one_or_none()
        if not db_submenu:
            raise SubmenuNotFound()
        db_submenu.title = self.submenu_update.title
        db_submenu.description = self.submenu_update.description
        self.db.commit()
        return db_submenu

    def delete_submenu(self):
        db_submenu = self.db.query(SubMenu).filter(SubMenu.id == self.submenu_id).first()
        self.db.delete(db_submenu)
        self.db.commit()








# def get_submenu(db: Session, menu_id: str, submenu_id: str):
#     submenu = db.query(Submenu).filter(menu_id == menu_id).filter(id == submenu_id).first()
#     if not submenu:
#         raise HTTPException(status_code=404, detail="Подменю не найдено")
#     result = jsonable_encoder(submenu)
#     result['dishes_count'] = 0


# def get_submenu_list(db: Session, menu_id: str):
#     all_submenu = db.query(Submenu).filter(menu_id == menu_id).all()
#     if not all_submenu:
#         return []
#     else:
#         list_submenu = [get_submenu(db, menu_id, submenu.id) for submenu in all_submenu]
#         return list_submenu


# def create_submenu(db: Session, menu_id: str, submenu: SubmenuCreate):
#     new_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
#     db.add(new_submenu)
#     db.commit()
#     return new_submenu


# def update_submenu(db: Session, menu_id: str, submenu_id: str, update_submenu: SubmenuUpdate):
#     db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
#     if not db_submenu:
#         raise HTTPException(status_code=404, detail="Подменю не найдено")
#     else:
#         db_submenu.title = update_submenu.title
#         db_submenu.description = update_submenu.description
#         db.add(db_submenu)
#         db.commit()
#     return db_submenu


# def delete_submenu(db: Session, menu_id: str, submenu_id: str):
#     db_submenu = db.query(Submenu).filter(Submenu.menu_id == menu_id).filter(Submenu.id == submenu_id).first()
#     db.delete(db_submenu)
#     db.commit()
