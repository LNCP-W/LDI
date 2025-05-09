from base import async_session
from db import DB


async def get_db():
    """
    Dependency for acquiring a database session within FastAPI endpoints.

    Yields:
        DB: Instance of DB class with an active async session.
    """
    async with async_session() as session:
        try:
            yield DB(session)
        except Exception as e:
            await session.rollback()
            raise e
