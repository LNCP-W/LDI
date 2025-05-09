from contextlib import asynccontextmanager
from typing import AsyncGenerator

from db import init_models
from fastapi import FastAPI
from routers.weather_router import router

# Disable the pylint warning for unused argument
# pylint: disable=unused-argument


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Initializes database models before the application starts.
    """
    await init_models()  # Initialize the database models
    yield


app = FastAPI(
    title="LDI",  # Title of the API application
    version="0.0.1",  # Version of the API
    lifespan=lifespan,  # Lifespan handler to manage startup/shutdown events
)

# Include weather-related API routes
app.include_router(router, prefix="/weather")
