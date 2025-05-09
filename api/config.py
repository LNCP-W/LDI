import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pydantic_settings import BaseSettings

Path("/mnt/log").mkdir(parents=True, exist_ok=True)
# Налаштування логування
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

# Ротація логів
log_handler = logging.handlers.RotatingFileHandler(
    "/mnt/log/app.log", maxBytes=10**6, backupCount=3
)

log_handler.setFormatter(log_formatter)


class DBConfig:
    """Database configuration."""

    host: str = "db"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    name: str = "postgres"

    class Config:
        """Configuration for database settings."""

        env_prefix = "DB_"

    @property
    def url(self) -> str:
        """
        Constructs the PostgreSQL connection URL using asyncpg driver.

        Returns:
            str: The constructed database connection URL.
        """
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )


class RedisConfig:
    """REDIS configuration."""

    host: str = "redis"
    port: int = 6379
    password: str = "1111"
    db: int = 0

    class Config:
        """Configuration for API settings."""

        env_prefix = "REDIS_"

    @property
    def url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"


class APIConfig:
    """API configuration."""

    city: str

    class Config:
        """Configuration for API settings."""

        env_prefix = "API_"


class ExternalAPIConfig:
    path: str = "http://api.weatherapi.com/v1/current.json?key={0}&q={1}"
    city: str = "Kyiv"
    key: str = "00751112dd4b4c1ba24121534250805"

    """External API configuration."""

    class Config:
        """Configuration for API settings."""

        env_prefix = "EXTAPI_"

    def url(self, city: str | None = None) -> str:
        if city is None:
            city = self.city
        return self.path.format(self.key, city)


class Settings(BaseSettings):
    """Basic application settings."""

    debug: bool = False
    db: DBConfig = DBConfig()
    api: APIConfig = APIConfig()
    redis: RedisConfig = RedisConfig()
    extapi: ExternalAPIConfig = ExternalAPIConfig()
    log_handler: RotatingFileHandler = log_handler

    loglevel: int = logging.INFO


config = Settings()
