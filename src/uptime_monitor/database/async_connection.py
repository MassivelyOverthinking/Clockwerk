#-------------------- Imports --------------------

from typing import AsyncGenerator, Tuple
from contextlib import asynccontextmanager
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker

from src.uptime_monitor.database.schemas import Base
from src.uptime_monitor.config.config_models import DatabaseConfig

#-------------------- Asynchronous DB --------------------

async def init_database(config: DatabaseConfig) -> Tuple[async_sessionmaker, AsyncEngine]:
    
    db_url = URL.create(
        drivername=config.driver_name,
        host=config.db_host_name,
        database=config.db_name,
        username=config.db_username,
        password=config.db_password,
        port=config.db_port
    )

    engine = create_async_engine(
        db_url,
        echo=config.echo_mode,
        pool_size=5,
        max_overflow=10
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=True)

    async with engine() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return sessionmaker, engine

@asynccontextmanager
async def get_session(sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        yield session