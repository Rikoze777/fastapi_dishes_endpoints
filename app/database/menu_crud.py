# from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database.db_exceptions import MenuNotFound
from app.database.models import Menu
from app.api.schemas import MenuCreate, MenuUpdate
from uuid import UUID


class MenuStorage:

    def __init__(self, db: Session, menu_id: UUID, menu_create=MenuCreate,
                 menu_update=MenuUpdate):
        self.db = db
        self.menu_id = menu_id
        self.menu_create = menu_create
        self.menu_update = menu_update

    def get_menu(self):
        menu = self.db.query(Menu).filter(Menu.id == self.menu_id).first()
        if not menu:
            raise MenuNotFound()
        return menu

    def get_list_menus(self):
        all_menu = self.db.query(Menu).all()
        return list(all_menu)

    def create_menu(self):
        new_menu = Menu(**self.menu_create.model_dump())
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def update(self):
        db_menu = self.db.query(Menu).filter(Menu.id == self.menu_id).first()
        db_menu.title = self.menu_update.title
        db_menu.description = self.menu_update.description
        self.db.add(db_menu)
        self.db.commit()
        return db_menu

    def delete(self):
        db_menu = self.db.query(Menu).filter(Menu.id == self.menu_id).first()
        if not db_menu:
            raise MenuNotFound()
        self.db.delete(db_menu)
        self.db.commit()




# def get_menu(db: Session, id: str):
#     menu = db.query(Menu).filter(Menu.id == id).first()
#     result = jsonable_encoder(menu)
#     if not menu:
#         raise HTTPException(status_code=404, detail="Меню не найдено")
#     submenus = db.query(Submenu).filter(Submenu.menu_id == id).all()
#     if not submenus:
#         result['submenus_count'] = 0
#         result['dishes_count'] = 0
#     else:
#         result['submenus_count'] = len(submenus)
#         result['dishes_count'] = 0
#     return result


# def get_menu_list(db: Session):
#     all_menu = db.query(Menu).all()
#     if not all_menu:
#         return []
#     else:
#         list_menu = [get_menu(db, menu.id) for menu in all_menu]
#         return list_menu


# def create_menu(db: Session, menu: MenuCreate):
#     new_menu = Menu(**menu.model_dump())
#     db.add(new_menu)
#     db.commit()
#     return new_menu


# def update_menu(db: Session, id: str, update_menu: MenuUpdate):
#     db_menu = db.query(Menu).filter(Menu.id == id).first()
#     db_menu.title = update_menu.title
#     db_menu.description = update_menu.description
#     db.add(db_menu)
#     db.commit()
#     return db_menu


# def delete_menu(db: Session, id: str):
#     db_menu = db.query(Menu).filter(Menu.id == id).first()
#     db.delete(db_menu)
#     db.commit()
