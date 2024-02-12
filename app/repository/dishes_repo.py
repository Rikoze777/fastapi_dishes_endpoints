from pydantic import UUID4
from sqlalchemy import delete
from sqlalchemy.future import select

from app.database.db import AsyncSession as AppAsyncSession
from app.database.models import Dishes
from app.repository.exceptions import DishExistsException
from app.schemas.schemas import Dishes as DishesModel
from app.schemas.schemas import DishesCreate, DishesUpdate


class DishesRepository:
    def __init__(self, session: AppAsyncSession):
        self.async_session: AppAsyncSession = session

    async def get_dish(self, submenu_id: UUID4, id: UUID4) -> Dishes:
        async with self.async_session.begin() as db_session:
            stmt = select(Dishes).where(Dishes.id == id)
            dish = await db_session.execute(stmt)
            dish = dish.scalars().first()
            if not dish:
                raise DishExistsException()
            dish = DishesModel.model_validate(dish)
            return dish

    async def create_dish(self, submenu_id: UUID4, dish: DishesCreate) -> Dishes:
        new_dish = Dishes(**dish.model_dump())
        new_dish.submenu_id = submenu_id
        new_dish.price = new_dish.price
        async with self.async_session.begin() as db_session:
            db_session.add(new_dish)
            await db_session.commit()
        return DishesModel.model_validate(new_dish)

    async def update_dish(
        self, submenu_id: UUID4, id: UUID4, update_dish: DishesUpdate
    ) -> DishesModel:
        async with self.async_session.begin() as db_session:
            stmt = select(Dishes).where(Dishes.id == id)
            dish = await db_session.execute(stmt)
            dish = dish.scalars().first()
            if not dish:
                raise DishExistsException()
            dish.title = update_dish.title
            dish.description = update_dish.description
            dish.price = f'{float(update_dish.price):.2f}'
            await db_session.flush()
            await db_session.refresh(dish)
            dish = DishesModel.model_validate(dish)
            return dish

    async def get_dishes_list(self, submenu_id: UUID4) -> list[Dishes]:
        async with self.async_session.begin() as db_session:
            stmt = select(Dishes).filter(Dishes.submenu_id == submenu_id)
            result = await db_session.execute(stmt)
            dishes = result.scalars().all()
            if not dishes:
                return []
            dishes_list = list(map(DishesModel.model_validate, dishes))
            for dish in dishes_list:
                dish.price = f'{float(dish.price):.2f}'
            return dishes_list

    async def delete_dish(self, submenu_id: UUID4, dish_id: UUID4) -> None:
        async with self.async_session.begin() as db_session:
            query = delete(Dishes).where(Dishes.id == dish_id)
            await db_session.execute(query)
            await db_session.commit()
