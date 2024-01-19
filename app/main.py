from fastapi import FastAPI
from routers.menu_router import router as menus_router
from database.db import engine
from database import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(menus_router, tags=["api"])
