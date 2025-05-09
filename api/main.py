import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from db import init_models
from fastapi import FastAPI
from routers.weather_router import router
from config import config
logger = logging.getLogger(__name__)
logger.setLevel(config.loglevel)
logger.addHandler(config.log_handler)


# Disable the pylint warning for unused argument
# pylint: disable=unused-argument


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Initializes database models before the application starts.
    """
    logger.info("Initializing database models...")
    await init_models()  # Initialize the database models
    logger.info("Database models initialized.")
    yield


app = FastAPI(
    title="LDI",  # Title of the API application
    version="0.0.1",  # Version of the API
    lifespan=lifespan,  # Lifespan handler to manage startup/shutdown events
)

logger.info("Starting FastAPI application...")

# Include weather-related API routes
app.include_router(router, prefix="/weather")
logger.info("Weather router included in the application.")
