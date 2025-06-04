#-------------------- Imports --------------------

import asyncio
import aiohttp
import logging
from aiohttp import ClientError, ClientTimeout

from time import perf_counter
from models import MonitorResult
from models import EmailConfig, Endpoint
from logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Monitor Function --------------------

@retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(ClientError, asyncio.TimeoutError),
        before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def _safe_session(session: aiohttp.ClientSession, url: str, timeout: int):
    async with session.get(url, timeout=ClientTimeout(total=timeout)) as resp:
        await resp.read()
        return resp


async def check_endpoint(session: aiohttp.ClientSession, endpoint: Endpoint, email_config: EmailConfig) -> MonitorResult:
    """
    Asynchronous function to monitor API Endpoint.
    Checks the specified Endpoint for general issues such as Outage and Latency.
    """
    
    url = str(endpoint.url)
    timeout = endpoint.timeout
    start = perf_counter()

    try:
        resp = await _safe_session(session, url, timeout)
        latency = perf_counter() - start
        logger.info("Endpoint check passed", extra={"endpoint": url, "latency": latency})

        return MonitorResult(
            endpoint_name=url,
            status_code=resp.status,
            latency=latency,
            success=resp.status == 200,
            error=None if resp.status == 200 else f"Unexpected status {resp.status}"
        )
    except Exception as err:
        latency = perf_counter() - start
        logger.exception("Unexpected exception occured")
        return MonitorResult(
            endpoint_name=url,
            status_code=0,
            latency=latency,
            success=False,
            error=str(err)
        )
