from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Config
from app.database.db import Base, async_engine
from app.routers.dishes_router import router as dishes_router
from app.routers.menu_router import router as menus_router
from app.routers.submenu_router import router as submenu_router

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    except Exception as error:
        print(error)


app = FastAPI(lifespan=lifespan)

app.include_router(menus_router, tags=['menu'])
app.include_router(submenu_router, tags=['submenu'])
app.include_router(dishes_router, tags=['dishes'])
