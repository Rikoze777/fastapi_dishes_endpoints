from typing import Union
from pydantic import BaseModel
from pydantic import UUID4


class Menu(BaseModel):
    id: UUID4
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdate(BaseModel):
    title: str
    description: str


class Submenu(BaseModel):
    id: UUID4
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuUpdate(BaseModel):
    title: str
    description: str


class Dishes(BaseModel):
    id: UUID4
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishesCreate(BaseModel):
    title: str
    description: str
    price: Union[str, float]

    class Config:
        orm_mode = True


class DishesUpdate(BaseModel):
    title: str
    description: str
    price: Union[str, float]

    class Config:
        orm_mode = True
