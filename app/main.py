from fastapi import FastAPI
from routers.menu_router import router as menus_router
from routers.submenu_router import router as submenu_router
from routers.dishes_router import router as dishes_router
from database.db import engine
from database import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menus_router, tags=["menu"])
app.include_router(submenu_router, tags=["submenu"])
app.include_router(dishes_router, tags=["dishes"])
