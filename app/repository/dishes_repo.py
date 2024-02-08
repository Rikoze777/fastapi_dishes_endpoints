from pydantic import UUID4
from sqlalchemy.future import select

from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Dishes
from app.repository.exceptions import DishExistsException
from app.schemas.schemas import DishesCreate, DishesUpdate


class DishesRepository:
    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_dish(self, submenu_id: UUID4, id: UUID4) -> Dishes:
        async with self.async_session.begin() as db_session:
            dish = await db_session.get(Dishes, (submenu_id, id))
            if not dish:
                raise DishExistsException()
            return dish

    async def create_dish(self, submenu_id: UUID4, dish: DishesCreate) -> Dishes:
        new_dish = Dishes(**dish.model_dump())
        new_dish.submenu_id = submenu_id
        new_dish.price = new_dish.price
        async with self.async_session.begin() as db_session:
            db_session.add(new_dish)
            await db_session.commit()
            return new_dish

    async def update_dish(
        self, submenu_id: UUID4, id: UUID4, update_dish: DishesUpdate
    ) -> Dishes:
        db_dish = await self.get_dish(submenu_id, id)
        db_dish.title = update_dish.title
        db_dish.description = update_dish.description
        db_dish.price = update_dish.price
        async with self.async_session.begin() as db_session:
            db_session.add(db_dish)
            await db_session.commit()
            return db_dish

    async def get_dishes_list(self, submenu_id: UUID4) -> list[Dishes]:
        async with self.async_session.begin() as db_session:
            stmt = select(Dishes).filter(Dishes.submenu_id == submenu_id)
            result = await db_session.execute(stmt)
            dishes = result.scalars().all()
            if not dishes:
                return []
            else:
                return dishes

    async def delete_dish(self, submenu_id: UUID4, dish_id: UUID4) -> None:
        db_dish = await self.get_dish(submenu_id, dish_id)
        async with self.async_session.begin() as db_session:
            db_session.delete(db_dish)
            await db_session.commit()
