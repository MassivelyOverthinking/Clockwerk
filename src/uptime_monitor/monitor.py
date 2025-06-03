#-------------------- Imports --------------------

import asyncio
import aiohttp

from time import perf_counter
from models import MonitorResult
from datetime import datetime
from models import EmailConfig, Endpoint, LoggerConfig
from logger import setup_logger

#-------------------- Logger Setup --------------------

log_config = LoggerConfig(
    log_level="INFO",
    log_file="monitor.log",
    log_to_file=True
)

logger = setup_logger(__name__, log_config)

#-------------------- Monitor Function --------------------

async def check_endpoint(session, endpoint: Endpoint, email_config: EmailConfig) -> MonitorResult:
    url = endpoint.url
    timeout = endpoint.timeout

    start = perf_counter()
    try:
        async with session.get(url, timeout=timeout) as resp:
            latency = perf_counter() - start
            return MonitorResult(
                endpoint_name=url,
                status_code=resp.status,
                latency=latency,
                success=resp.status == 200,
                error=None if resp.status == 200 else f"Unexpected status {resp.status}"
            )
    except Exception as err:
        latency = perf_counter() - start
        logger.info(f"Unexpected exception occured {err}")
        return MonitorResult(
            endpoint_name=url,
            status_code=0,
            latency=latency,
            success=False,
            error=str(err)
        )
