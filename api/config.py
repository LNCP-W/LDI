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

    @property
    def url(self):
        """
        Constructs the PostgreSQL connection URL using asyncpg driver.

        Returns:
            str: The constructed database connection URL.
        """
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )


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
