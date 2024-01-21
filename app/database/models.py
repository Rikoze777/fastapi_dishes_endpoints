import uuid
from sqlalchemy import Column, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))
    menu_id = Column(UUID, ForeignKey('menus.id', ondelete='CASCADE'))

    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')
    menu = relationship('Menu', back_populates='submenus')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title = Column(String(128), unique=True, nullable=False)
    description = Column(String(256))
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    submenu_id = Column(UUID, ForeignKey('submenus.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dishes')




# import uuid
# from sqlalchemy import Column, String, ForeignKey, DECIMAL, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects.postgresql import UUID


# Base = declarative_base()


# class Menu(Base):
#     __tablename__ = "menu"

#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     title = Column(String)
#     description = Column(String)


# class Submenu(Base):
#     __tablename__ = 'submenu'

#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     title = Column(String)
#     description = Column(String)
#     dishes_count = Column(Integer)
#     menu_id = Column(String, ForeignKey('menu.id',
#                      ondelete='CASCADE'), nullable=False)


# class Dishes(Base):
#     __tablename__ = 'dishes'

#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid.uuid4,
#     )
#     title = Column(String)
#     description = Column(String)
#     price = Column(DECIMAL, nullable=False, scale=2)
#     submenu_id = Column(String, ForeignKey('menu.id',
#                         ondelete='CASCADE'), nullable=False)

# from sqlalchemy.orm import relationship