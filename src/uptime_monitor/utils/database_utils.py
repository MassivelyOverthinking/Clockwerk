#-------------------- Imports --------------------

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.uptime_monitor.models import MonitorResult
from src.uptime_monitor.database.async_connection import get_session
from src.uptime_monitor.database.schemas import MonitorHistory
from src.uptime_monitor.utils.common import update_endpoint
from src.uptime_monitor.logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Utility Functions --------------------

async def write_to_db(result: MonitorResult, sessionmaker: async_sessionmaker):
    async with get_session(sessionmaker) as session:
        try:
            history_entry = MonitorHistory(
                url=result.endpoint_name,
                timestamp=result.timestamp,
                status_code=result.status_code,
                latency=result.latency,
                success=result.success,
                error=result.error
            )
            session.add(history_entry)
            endpoint_status = await update_endpoint(session, result)
            session.add(endpoint_status)

            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            logger.exception(f"Database operation failed: {err}")
        finally:
            await session.close()