from config import config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Create an asynchronous SQLAlchemy engine using configuration values
engine = create_async_engine(config.db.url, future=True, echo=config.debug)

# Create an asynchronous session maker for managing DB sessions
async_session = async_sessionmaker(engine, class_=AsyncSession)

# Base class for ORM models
Base: type = declarative_base()
