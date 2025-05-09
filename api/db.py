from datetime import date, datetime, time
from typing import Any

from base import Base, engine
from models.weather_model import Weather
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


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
        weather = Weather(city=city, temperature=temperature, time_point=time_point)
        self.db_session.add(weather)
        await self.db_session.commit()
        await self.db_session.refresh(weather)
        return int(weather.id)

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

        command = (
            select(Weather)
            .where(and_(Weather.city == city, Weather.time_point.between(start, end)))
            .order_by(Weather.time_point.desc())
        )

        result = await self.db_session.execute(command)
        return list(result.scalars().all())


async def init_models() -> None:
    """Initialize database models."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
