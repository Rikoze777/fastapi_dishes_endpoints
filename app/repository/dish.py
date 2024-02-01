from pydantic import UUID4
from app.crud.exceptions import DishExistsException
from app.schemas.schemas import DishesUpdate, DishesCreate
from sqlalchemy.ext.asyncio import async_session, AsyncSession
from app.database.models import Dishes


class DishRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dish(self,
                       submenu_id: UUID4,
                       id: UUID4) -> Dishes:
        async with async_session(self.db) as session:
            dish = await session.get(Dishes, (submenu_id, id))
            if not dish:
                raise DishExistsException()
            return dish

    async def create_dish(self,
                          submenu_id: UUID4,
                          dish: DishesCreate) -> Dishes:
        new_dish = Dishes(**dish.model_dump())
        new_dish.submenu_id = submenu_id
        new_dish.price = new_dish.price
        async with async_session(self.db) as session:
            session.add(new_dish)
            await session.commit()
            return new_dish

    async def update_dish(self,
                          submenu_id: UUID4,
                          id: UUID4,
                          update_dish: DishesUpdate) -> Dishes:
        db_dish = await self.get_dish(submenu_id, id)
        db_dish.title = update_dish.title
        db_dish.description = update_dish.description
        db_dish.price = update_dish.price
        async with async_session(self.db) as session:
            session.add(db_dish)
            await session.commit()
            return db_dish

    async def get_dishes_list(self,
                              submenu_id: UUID4) -> list[Dishes]:
        async with async_session(self.db) as session:
            all_dishes = await session.query(Dishes).filter(Dishes.submenu_id == submenu_id).all()
            if not all_dishes:
                return []
            else:
                return all_dishes

    async def delete_dish(self,
                          submenu_id: UUID4,
                          dish_id: UUID4) -> None:
        db_dish = await self.get_dish(submenu_id, dish_id)
        async with async_session(self.db) as session:
            session.delete(db_dish)
            await session.commit()
