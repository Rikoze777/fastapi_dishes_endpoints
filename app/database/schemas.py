from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class Menu(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdate(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    id: UUID
    title: str
    description: str
    dishes_count: int

    class Config:
        from_attributes = True


class SubmenuCreate(BaseModel):
    title: str
    description: str
    dishes_count: int


class SubmenuUpdate(BaseModel):
    title: str
    description: str


class Dishes(BaseModel):
    id: str
    title: str
    description: str
    price: float

    class Config:
        from_attributes = True



class DishesCreate(BaseModel):
    title: str
    description: str
    price: float