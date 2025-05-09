from base import Base
from sqlalchemy import Column, DateTime, Float, Integer, String


class Weather(Base):
    """
    ORM model for storing weather data.

    Attributes:
        id (int): Primary key identifier.
        city (str): City name.
        time_point (datetime): Timestamp of the temperature measurement.
        temperature (float): Recorded temperature value.
    """

    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    time_point = Column(DateTime, nullable=False, index=True)
    temperature = Column(Float, nullable=False)
