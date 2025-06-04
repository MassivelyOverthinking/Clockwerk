#-------------------- Imports --------------------

from typing import Optional, AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from contextlib import asynccontextmanager
from src.uptime_monitor.models import DatabaseConfig

#-------------------- Global Variables --------------------

_engine = Optional[AsyncEngine] = None
_sessionmaker = Optional[sessionmaker[AsyncSession]] = None

#-------------------- Configuration & Initialization --------------------

def init_database(config: DatabaseConfig):
    """
    Initialize database engine and session factory if database is activated.
    Call this once at app startup.
    """

    global _engine, _sessionmaker

    if not config.db_activation:
        return 
    
    db_url = URL.create(
        drivername=config.driver_name,
        host=config.db_host_name,
        database=config.db_name,
        username=config.db_username,
        password=config.db_password,
        port=config.db_port
    )

    _engine = create_async_engine(db_url, echo=config.echo_mode)
    _sessionmaker = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=True)


#-------------------- AsyncSession Access --------------------

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an AsyncSession using the configured sessionmaker.
    Usage: async with get_session() as session:
    """
    if _sessionmaker is None:
        raise RuntimeError("Database not initialized. Call init_databse() first")
    
    async with _sessionmaker() as session:
        yield session

#-------------------- Database Shutdown --------------------

async def shutdown_engine():
    """
    Call this at shutdown to dispose of the async engine properly.
    """
    if _engine is not None:
        await _engine.dispose()



