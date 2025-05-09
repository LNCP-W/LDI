import logging
from datetime import date, datetime, time

from base import Base, engine
from config import config
from models.weather_model import Weather
from schema.wether_schema import WetherSchema
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
logger.setLevel(config.loglevel)
logger.addHandler(config.log_handler)


class DB:
    """
    Database access layer for weather-related operations.

    Methods:
        set_weather(city, temperature, time): Saves a new weather record.
        get_weather(city, day): Retrieves weather data for a given city and day.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize DB handler with SQLAlchemy async session.

        Args:
            session (AsyncSession): Async database session.
        """
        self.db_session = session
        logger.info("Database session initialized.")

    async def set_weather(
        self,
        city: str,
        temperature: float,
        time_point: datetime = datetime.now(tz=None),
    ) -> int | None:
        """
        Store weather data in the database.

        Args:
            city (str): City name.
            temperature (float): Temperature to store.
            time_point (datetime): Time of the measurement (defaults to now).

        Returns:
            int: ID of the newly created record.
        """
        logger.info(
            "Saving weather data: city=%s, temperature=%s, time_point=%s",
            city,
            temperature,
            time_point,
        )

        weather = Weather(city=city, temperature=temperature, time_point=time_point)
        self.db_session.add(weather)
        await self.db_session.commit()
        await self.db_session.refresh(weather)
        logger.info("Weather data saved with ID: %s", weather.id)
        return int(weather.id)

    async def get_weather(
        self, city: str, day: date = date.today()
    ) -> list[WetherSchema]:
        """
        Retrieve weather records for a given city and specific day.

        Args:
            city (str): City name to filter records.
            day (datetime): Day for which data is requested (defaults to today).

        Returns:
            List[Weather]: List of matching weather records ordered by time descending.
        """
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        logger.info("Retrieving weather for city=%s on day=%s", city, day)

        command = (
            select(Weather)
            .where(and_(Weather.city == city, Weather.time_point.between(start, end)))
            .order_by(Weather.time_point.desc())
        )

        result = await self.db_session.execute(command)
        records = list(result.scalars().all())
        weather_list = [WetherSchema.model_validate(i) for i in records]
        logger.info("Retrieved %d weather records.", len(records))
        return weather_list


async def init_models() -> None:
    """Initialize database models."""
    logger.info("Initializing database models...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database models initialized successfully.")
