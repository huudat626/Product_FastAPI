from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "PRODUCTS Intro"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "PRODUCTS"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()