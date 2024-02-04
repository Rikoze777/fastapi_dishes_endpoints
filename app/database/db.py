from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config
import redis


config = Config()
database_url = config.POSTGRES_URL
engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_redis():
    cache = redis.Redis(host='redis', port=6379)
    return cache


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
