#-------------------- Imports --------------------

import asyncio
import aiohttp

from time import perf_counter
from models import MonitorResult
from datetime import datetime

#-------------------- Monitor Function --------------------

async def check_endpoint(session, endpoint: dict) -> MonitorResult:
    url = endpoint["url"]
    timeout = endpoint.get("timeout", 3)

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
        return MonitorResult(
            endpoint_name=url,
            status_code=0,
            latency=latency,
            success=False,
            error=str(err)
        )
