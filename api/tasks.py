import asyncio
import logging

import httpx
from base import async_session
from celery import Celery
from config import config
from db import DB

logger = logging.getLogger(__name__)
logger.setLevel(config.loglevel)
logger.addHandler(config.log_handler)

celery_app = Celery(
    "celery_worker",
    broker=config.redis.url,
    backend=config.redis.url,
)


def get_data_from_resp(resp: httpx.Response) -> float:
    """
    Extract temperature data from the API response.
    """
    resp_json = resp.json()
    temp = resp_json["current"]["temp_c"]
    logger.info("Extracted temperature: %.2f°C", temp)
    return float(temp)


@celery_app.task  # type: ignore[misc]
def fetch_and_store_data() -> None:
    """
    Celery task to fetch and store weather data.
    """
    logger.info("Starting fetch_and_store_data task")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_fetch_and_store_data_async())


async def _fetch_and_store_data_async() -> None:
    """
    Asynchronous function to fetch weather data and store it in the database.
    """
    logger.info("Fetching weather data from external API...")
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(config.extapi.url())
            response.raise_for_status()
            logger.info("Received weather data successfully.")
        except httpx.RequestError as e:
            logger.error("Error occurred while acquiring DB session: %s", e)
            raise

    async with async_session() as session:
        try:
            db = DB(session)
            temperature = get_data_from_resp(response)
            await db.set_weather(config.extapi.city, temperature)
            await session.commit()
            logger.info(
                "Weather data for %s saved to the database.", config.extapi.city
            )

        except Exception as e:
            await session.rollback()
            logger.error("Failed to store weather data: %s", e)
            raise


if __name__ == "__main__":
    logger.info("Starting weather fetch and store process...")
    asyncio.run(_fetch_and_store_data_async())
