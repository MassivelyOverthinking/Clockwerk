#-------------------- Imports --------------------

import json
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.uptime_monitor.models import MonitorResult
from database.db_connection import get_session
from database.schemas import EndpointStatus

from src.uptime_monitor.logger import get_logger

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