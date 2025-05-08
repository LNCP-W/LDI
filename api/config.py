from pydantic_settings import BaseSettings


class DBConfig:
    """Database configuration."""

    host: str = "db"
    port: int = 5432
    user: str
    password: str
    name: str

    class Config:
        """Configuration for database settings."""

        env_prefix = "DB_"


class APIConfig:
    """API configuration."""

    city: str

    class Config:
        """Configuration for API settings."""

        env_prefix = "API_"


class Settings(BaseSettings):
    """Basic application settings."""

    debug: bool = False
    db: DBConfig = DBConfig()
    api: APIConfig = APIConfig()


config = Settings()
