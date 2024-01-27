from pydantic_settings import BaseSettings


class Config(BaseSettings):

    PROD_DB_NAME: str
    PROD_DB_USER: str
    PROD_DB_PASSWORD: str
    PROD_DB_HOST: str
    PROD_DB_PORT: str

    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: str

    class Config:
        env_file = "./.env"
