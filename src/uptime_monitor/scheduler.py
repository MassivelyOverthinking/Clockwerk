#-------------------- Imports --------------------

import asyncio
import aiohttp

from src.uptime_monitor.monitor import check_endpoint
from src.uptime_monitor.reporter import handle_result
from src.uptime_monitor.config.config_models import EmailConfig, MonitorConfig, DatabaseConfig
from src.uptime_monitor.logger import get_logger

from src.uptime_monitor.database.db_connection import shutdown_engine

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
        if db_config.db_activation:
            await shutdown_engine()
        logger.info(f"Scheduling loop cleanup is complete")