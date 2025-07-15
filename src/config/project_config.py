import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION: str = os.getenv("VERSION")
    DEBUG: bool = os.getenv("DEBUG")
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS")

    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: int = os.getenv("POSTGRES_PORT")
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_DRIVER: str = os.getenv("POSTGRES_DRIVER")
    DB_NAME: str = os.getenv("POSTGRES_DB")

    CACHE_HOST: str = os.getenv("POSTGRES_DB")
    CACHE_PORT: int = os.getenv("POSTGRES_DB")
    CACHE_DB: int = os.getenv("POSTGRES_DB")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ENCODE_ALGORITHM: str = os.getenv("JWT_ENCODE_ALGORITHM")

    @property
    def db_url(self) -> str:
        return (f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


