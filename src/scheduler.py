#-------------------- Imports --------------------

import asyncio
import aiohttp

from monitor import check_endpoint
from reporter import handle_result
from config import CHECK_INTERVAL, ENDPOINTS

#-------------------- Scheduler Function --------------------

async def scheduling_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [check_endpoint(session=session, endpoint=ep) for ep in ENDPOINTS]
            results = await asyncio.gather(*tasks)
            
            await asyncio.gather(*(handle_result(result) for result in results))
            
            await asyncio.sleep(CHECK_INTERVAL)