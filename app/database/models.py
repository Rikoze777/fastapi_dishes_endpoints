import uuid
from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        String,
        default=str(uuid.uuid4()),
        primary_key=True)
    title = Column(String)
    description = Column(String)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(
        String,
        default=str(uuid.uuid4()),
        primary_key=True)
    title = Column(String)
    description = Column(String)
    dishes_count = Column(Integer)
    menu_id = Column(String, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(
        String,
        default=str(uuid.uuid4()),
        primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float, nullable=False, default=0.00)
    submenu_id = Column(String, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False)