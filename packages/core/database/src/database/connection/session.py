# packages/core/database/src/database/connection/session.py

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


def create_db_engine(database_url: str, echo: bool = False) -> AsyncEngine:
    """
    Creates and returns the SQLAlchemy asynchronous engine.
    """
    return create_async_engine(database_url, echo=echo)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker:
    """
    Creates and returns the session factory bound to the given engine.
    """
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )
