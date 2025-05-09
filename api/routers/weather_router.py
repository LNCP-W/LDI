import logging
from datetime import date
from typing import Any

from db import DB
from dependencies import get_db, verify_token
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from config import config

logger = logging.getLogger(__name__)
logger.setLevel(config.loglevel)
logger.addHandler(config.log_handler)

# Create a router with a global dependency on token verification
router = APIRouter(dependencies=[Depends(verify_token)], tags=["weather"])


@router.get(
    "/",
    summary="Get weather data",
    response_description="List of weather records for a specific city and date",
    response_class=JSONResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "city": "Kyiv",
                            "time": "2025-05-08T14:00:00",
                            "temperature": 21.5,
                        }
                    ]
                }
            },
        },
        401: {"description": "Unauthorized"},
        403: {"description": "Not authenticated"},
    },
)
async def weather(
    city: str = Query(default="Kyiv", description="City name"),
    day: date = Query(
        default_factory=date.today, description="Date in YYYY-MM-DD format"
    ),
    db: DB = Depends(get_db),
) -> list[Any] | None:
    """
    Retrieve weather data for a specified city and day.

    - **city**: Name of the city to query weather data for (default is "Kyiv")
    - **day**: Date to filter weather records (default is today)

    Returns a list of weather entries matching the criteria.
    """
    logger.info(f"Received weather data request for city: {city}, date: {day}")

    try:
        weather_data = await db.get_weather(city, day)
        logger.info(f"Fetched {len(weather_data)} weather records for {city} on {day}.")
        return weather_data
    except Exception as e:
        logger.error(f"Error occurred while fetching weather data for {city} on {day}: {e}")
        raise e
