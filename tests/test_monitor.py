import pytest
import asyncio
from aiohttp import ClientSession
from src.uptime_monitor.models import Endpoint
from src.uptime_monitor.monitor import check_endpoint
from src.uptime_monitor.config.config_models import EmailConfig

@pytest.mark.asyncio
async def test_check_endpoint_success():
    endpoint = Endpoint(
        url="https://httpbin.org/status/200",
        timeout=3, 
        alert_threshold=3
    )
    config = EmailConfig(
        smtp_host="smtp.mailtrap.io",
        smtp_port=587,
        email_from="test@example.com",
        email_to="HysingerDev@gmail.com"
    )
    
    async with ClientSession() as session:
        result = await check_endpoint(session, endpoint, config)

    assert result.endpoint_name == "https://httpbin.org/status/200"
    assert result.success is True
    assert result.status_code == 200
    assert result.latency is not None
    assert result.error is None


