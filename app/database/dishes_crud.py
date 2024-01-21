from typing import List, Union
from uuid import UUID
from app.api.schemas import DishesCreate, DishesUpdate
from sqlalchemy.orm import Session
from app.database.models import Dish
from app.database.db_exceptions import DishNotFound


class DishesStorage:

    def __init__(self, db: Session, submenu_id: UUID,
                 menu_id: UUID, dish_id: UUID,
                 dish_create=DishesCreate,
                 dish_update=DishesUpdate):
        self.db = db.Session()
        self.submenu_id = submenu_id
        self.menu_id = menu_id
        self.dish_id = dish_id
        self.dish_create = dish_create
        self.dish_update = dish_update

    def get_dish(self) -> Union[Dish, None]:
        dish = self.db.query(Dish).filter(Dish.id == self.dish_id).scalar_one_or_none()
        if not dish:
            raise DishNotFound()
        return dish

    def get_list_dishes(self) -> List[Dish]:
        list_dishes = self.db.query(Dish).filter(Dish.submenu_id == self.submenu_id).scalars().all()
        if not list_dishes:
            list_dishes = []
        return list_dishes

    def create(self) -> Dish:
        new_dish = Dish(**self.dish_create.model_dump())
        new_dish.price = round(self.dish_create.price, 2)
        new_dish.submenu_id = self.submenu_id
        self.db.add(new_dish)
        self.db.commit()
        return new_dish

    def update(self) -> Union[Dish, None]:
        db_dish = self.db.query(Dish).filter(Dish.id == id).scalar()
        if not db_dish:
            raise DishNotFound()
        self.db.merge(self.dish_update)
        self.db.commit()
        return self.dish_update

    def delete(self, db: Session, id: UUID):
        db.query(Dish).filter(Dish.id == id).delete(synchronize_session=False)
        db.commit()




# def get_dish(db: Session, submenu_id: str, id: str):
#     dish = db.query(Dishes).filter(Dishes.id == id).scalar()
#     if not dish:
#         raise HTTPException(status_code=404, detail="Блюдо не найдено")
#     return dish


# # Создать блюдо
# def create_dish(db: Session, submenu_id: str, dish: DishesCreate):
#     new_dish = Dishes(**dish.model_dump())
#     new_dish.price = round(dish.price, 2)
#     new_dish.submenu_id = submenu_id
#     db.add(new_dish)
#     db.commit()
#     return new_dish


# # Обновить блюдо
# def update_dish(db: Session, submenu_id: str, id: str, update_dish: DishesCreate):
#     db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
#     if not db_dish:
#         raise HTTPException(status_code=404, detail="Меню не найдено")
#     else:
#         db_dish.title = update_dish.title
#         db_dish.description = update_dish.description
#         db_dish.price = round(update_dish.price, 2)
#         db.add(db_dish)
#         db.commit()
#     return db_dish


# # Просмотр списка блюд
# def get_dishes_list(db: Session, submenu_id: str):
#     all_dishes = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).all()
#     if not all_dishes:
#         return []
#     else:
#         list_dishes = [get_dish(db, submenu_id, dish.id) for dish in all_dishes]
#         return list_dishes


# # Удаление блюда
# def delete_dish(db: Session, submenu_id: str, id: str):
#     db_dish = db.query(Dishes).filter(Dishes.submenu_id == submenu_id).filter(Dishes.id == id).first()
#     db.delete(db_dish)
#     db.commit()