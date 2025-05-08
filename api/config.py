from pydantic_settings import BaseSettings


class DBConfig:
    host: str = "db"
    port: int = 5432
    user: str
    password: str
    name: str

    class Config:
        env_prefix = "DB_"


class APIConfig:
    city: str

    class Config:
        env_prefix = "API_"


class Settings(BaseSettings):
    debug: bool = False
    db: DBConfig = DBConfig()
    api: APIConfig = APIConfig()


config = Settings()
