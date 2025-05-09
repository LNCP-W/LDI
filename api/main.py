import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from config import config
from db import init_models
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routers.weather_router import router
from starlette.exceptions import HTTPException as StarletteHTTPException

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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    logger.error("HTTP error: %s", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "HTTPException"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "error": "ValidationError"},
    )


logger.info("Starting FastAPI application...")

# Include weather-related API routes
app.include_router(router, prefix="/weather")
logger.info("Weather router included in the application.")
