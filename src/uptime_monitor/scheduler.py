#-------------------- Imports --------------------

import asyncio
import aiohttp

from monitor import check_endpoint
from reporter import handle_result
from models import EmailConfig, MonitorConfig, LoggerConfig
from logger import get_logger

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Scheduler Function --------------------

async def scheduling_loop(monitor_config: MonitorConfig, email_config: EmailConfig):
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [check_endpoint(session=session, endpoint=ep, email_config=email_config) for ep in monitor_config.endpoints]
            results = await asyncio.gather(*tasks)
            
            await asyncio.gather(*(handle_result(result, monitor_config, email_config) for result in results))
            
            await asyncio.sleep(monitor_config.check_interval)