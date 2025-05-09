import logging
import re
from typing import AsyncGenerator

from base import async_session
from config import config
from db import DB
from fastapi import Depends, HTTPException, Request, status

logger = logging.getLogger(__name__)
logger.setLevel(config.loglevel)
logger.addHandler(config.log_handler)


async def get_db() -> AsyncGenerator[DB, None]:
    """
    Dependency for acquiring a database session within FastAPI endpoints.

    Yields:
        DB: Instance of DB class with an active async session.
    """
    async with async_session() as session:
        try:
            logger.info("Acquiring new DB session")
            yield DB(session)
        except Exception as e:
            logger.error("Error occurred while acquiring DB session: %s", e)
            await session.rollback()
            raise e


async def get_token(request: Request) -> str:
    """
    Extracts the token from the 'x-token' header of the request.
    Raises an HTTP 403 error if the token is missing.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        str: The extracted token.

    Raises:
        HTTPException: If the 'x-token' header is not present.
    """
    token = request.headers.get("x-token")
    if token:
        logger.info("Token found in request headers")
        return token
    logger.warning("Token missing in request headers")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
    )


async def verify_token(token: str = Depends(get_token)) -> bool:
    """
    Verifies that the token is a valid 32-character alphanumeric string.
    Raises an HTTP 401 error if the token format is invalid.

    Args:
        token (str): The token to verify.

    Returns:
        bool: True if the token is valid.

    Raises:
        HTTPException: If the token format is invalid.
    """
    pattern = r"^[a-zA-Z0-9]{32}$"
    if re.match(pattern, token):
        logger.info("Token verified successfully")
        return True
    logger.warning("Invalid token format")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token"
    )
