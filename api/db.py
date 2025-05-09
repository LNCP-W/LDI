import logging
from datetime import date, datetime, time
from typing import Any

from base import Base, engine
from models.weather_model import Weather
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from config import config

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
        logger.info(f"Saving weather data: {city=}, {temperature=}, {time_point=}")
        try:
            weather = Weather(city=city, temperature=temperature, time_point=time_point)
            self.db_session.add(weather)
            await self.db_session.commit()
            await self.db_session.refresh(weather)
            logger.info(f"Weather data saved with ID: {weather.id}")
            return int(weather.id)
        except Exception as e:
            logger.error(f"Failed to save weather data: {e}")
            await self.db_session.rollback()
            return None

    async def get_weather(
        self, city: str, day: date = date.today()
    ) -> list[Any] | None:
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
        logger.info(f"Retrieving weather for {city=} on {day=}")

        try:
            command = (
                select(Weather)
                .where(and_(Weather.city == city, Weather.time_point.between(start, end)))
                .order_by(Weather.time_point.desc())
            )

            result = await self.db_session.execute(command)
            records = list(result.scalars().all())
            logger.info(f"Retrieved {len(records)} weather records.")
            return records
        except Exception as e:
            logger.error(f"Failed to retrieve weather data: {e}")
            return None


async def init_models() -> None:
    """Initialize database models."""
    logger.info("Initializing database models...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database models initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}")
