import pytest

from unittest.mock import patch, AsyncMock

from src.uptime_monitor.utils.database_utils import write_to_db
from src.uptime_monitor.models import MonitorResult
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_write_to_db():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_sessionmaker = AsyncMock(return_value=mock_session)

    result = MonitorResult(
        endpoint_name="https://example.com",
        latency=0.5,
        status_code=200,
        success=True
    )

    with patch("src.uptime_monitor.utils.database_utils.get_session", return_value=mock_session):
        await write_to_db(result, mock_sessionmaker)
    
    assert mock_session.add.call_count == 2
    mock_session.commit.assert_awaited_once()