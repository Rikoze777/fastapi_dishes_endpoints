import uuid
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        String,
        default=str(uuid.uuid4()),
        primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
