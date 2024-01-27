from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    TESTBASE_URL: str

    class Config:
        env_file = "./.env"
