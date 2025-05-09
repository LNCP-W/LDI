import asyncio

import httpx
from base import async_session
from celery import Celery
from config import config
from db import DB

celery_app = Celery(
    "celery_worker",
    broker=config.redis.url,
    backend=config.redis.url,
)


def get_data_from_resp(resp: httpx.Response) -> float:
    resp_json = resp.json()
    temp = resp_json["current"]["temp_c"]

    return float(temp)


@celery_app.task  # type: ignore[misc]
def fetch_and_store_data() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_fetch_and_store_data_async())


async def _fetch_and_store_data_async() -> None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(config.extapi.url())
        response.raise_for_status()
    async with async_session() as session:
        try:
            db = DB(session)
            await db.set_weather(config.extapi.city, get_data_from_resp(response))
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e


if __name__ == "__main__":
    asyncio.run(_fetch_and_store_data_async())
