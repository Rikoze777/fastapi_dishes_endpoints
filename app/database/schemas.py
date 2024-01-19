from pydantic import BaseModel
from uuid import UUID


class Menu(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuUpdate(BaseModel):
    title: str
    description: str
