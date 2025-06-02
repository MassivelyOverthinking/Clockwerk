#-------------------- Imports --------------------

from dataclasses import dataclass, field
from datetime import datetime

#-------------------- Monitor Result --------------------

@dataclass
class MonitorResult:
    endpoint_name: str = None
    timestamp: datetime = field(default_factory=datetime.now())
    status_code: int = None
    latency: float = None
    success: bool = False
    error: str = None
