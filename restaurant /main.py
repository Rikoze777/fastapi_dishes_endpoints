from fastapi import FastAPI
from .routers.menu_router import router as menus_router

app = FastAPI()

app.include_router(menus_router, prefix="/api", tags=["api"])
