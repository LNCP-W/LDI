from celery import Celery

from api.config import config

celery_app = Celery("beat_worker", broker=config.redis.url, backend=config.redis.url)

celery_app.conf.beat_schedule = {
    "fetch-every-hour": {
        "task": "api.tasks.fetch_and_store_data",
        "schedule": 20.0,
    },
}

celery_app.conf.timezone = "UTC"
