#-------------------- Imports --------------------

import asyncio
import aiohttp

from monitor import check_endpoint
from reporter import handle_result
from config.config_models import EmailConfig, MonitorConfig, DatabaseConfig
from logger import get_logger

from database.db_connection import shutdown_engine

#-------------------- Logger Setup --------------------

logger = get_logger()

#-------------------- Scheduler Function --------------------

async def scheduling_loop(monitor_config: MonitorConfig, email_config: EmailConfig, db_config: DatabaseConfig):
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [check_endpoint(session=session, endpoint=ep, email_config=email_config) for ep in monitor_config.endpoints]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                await asyncio.gather(*(handle_result(result, monitor_config, email_config, db_config) for result in results))
                logger.info("All Endpoints have been checked and appropriate measures taken!")
                
                await asyncio.sleep(monitor_config.check_interval)
                logger.info(f"Scheduling loop returning to sleep for {monitor_config.check_interval} seconds")
    except asyncio.CancelledError:
        logger.info(f"Scheduling loop is shutting down...")
    finally:
        for task in asyncio.all_tasks():
            task.cancel()
        if db_config.db_activation:
            await shutdown_engine()