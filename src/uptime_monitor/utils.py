#-------------------- Imports --------------------

import json
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import MonitorResult, DatabaseConfig
from database.db_connection import get_session
from database.schemas import MonitorHistory, EndpointStatus

from logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Utility Functions --------------------

def create_msg(result: MonitorResult) -> str:
    alert_msg = {
        "Endpoint": result.endpoint_name,
        "Timestamp": str(result.timestamp),
        "Status": "OUTAGE" if not result.success else "HIGH LATENCY",
        "Status code": result.status_code,
        "Latency": result.latency,
        "Error": result.error
    }
    return json.dumps(alert_msg, indent=2, sort_keys=True, ensure_ascii=True)

async def write_to_db(result: MonitorResult, config: DatabaseConfig):
    async with get_session() as session:
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
            logger.exception(f"Database operation failed: {err}")

async def update_endpoint(session: AsyncSession, result: MonitorResult):
    status = "UP" if result.success else "DOWN"
    stmt = select(EndpointStatus).where(EndpointStatus.url == result.endpoint_name)
    res = await session.execute(stmt)
    existing = res.scalar_one_or_none()

    if existing:
        existing.current_status = status
        existing.last_updated = datetime.now(timezone.utc)
        return existing
    else:
        new_status = EndpointStatus(
            url=result.endpoint_name,
            current_status=status,
            last_updated=datetime.now(timezone.utc)
        )
        return new_status