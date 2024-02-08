import uuid

from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.db import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)

    menu_id = Column(UUID(as_uuid=True),
                     ForeignKey('menu.id', ondelete='CASCADE'))


class Dishes(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(DECIMAL(10, 2), nullable=False)

    submenu_id = Column(UUID(as_uuid=True),
                        ForeignKey('submenu.id', ondelete='CASCADE'))
