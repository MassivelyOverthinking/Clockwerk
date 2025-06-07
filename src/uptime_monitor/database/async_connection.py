#-------------------- Imports --------------------

from typing import Tuple
from contextlib import asynccontextmanager
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from src.uptime_monitor.database.schemas import Base
from src.uptime_monitor.config.config_models import DatabaseConfig

#-------------------- Asynchronous DB --------------------

async def init_database(config: DatabaseConfig) -> Tuple[async_sessionmaker, AsyncEngine]:
    """
    Summary:
        Function used to initialize database connection and creation of schemas.

    Description:
    - Utilises DatabaseConfig-object to enable database connection, if enabled.
    - Produces final database connection string and uses it create SQLalchemy engine.
    - Engine produces an asynchronous sessionmaker-object passed to subsequent functions.
    - Both engine and sessionmaker objects are passed down through the layers.

    Args:
        config (DatabaseConfig): Configuration model providing the necessary information to initiate database connection.
    
    Returns:
        sessionmaker (async_sessionmaker): SQLalchemy's asynchronous sessionmaker used to create DB sessions.
        engine (AsyncEngine): Asynchronous database engine handling the connection pool.

    Raises:
        None
    """
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
    """
    Summary:
        An asynchronous generator-function used to provide sessions for database queries.

    Description:
    - Utilises a With statemtent to safely construct and close async DB sessions.

    Args:
        sessionmaker (async_sessionmaker): Used by the generator function to provide multiple async DB session.

    Returns (Yields):
        session: SQLalchemy's asynchronous session object used for database querying.

    Raises:
        None
    """
    async with sessionmaker() as session:
        yield session