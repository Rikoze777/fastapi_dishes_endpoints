from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config


config = Config()
database_url = config.POSTGRES_URL
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
