#-------------------- Imports --------------------

from models import MonitorResult
from config import LATENCY_THRESHOLD

#-------------------- Utility Functions --------------------

def create_msg(result: MonitorResult) -> dict[str]:
    alert_msg = {
        "Endpoint": result.endpoint_name,
        "Timestamp": str(result.timestamp),
        "Status": "OUTAGE" if not result.success else "HIGH LATENCY",
        "Status code": result.status_code,
        "Latency": result.latency,
        "Error": result.error
    }
    return alert_msg