#-------------------- Imports --------------------

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, AnyHttpUrl


#-------------------- Monitor Result --------------------

class MonitorResult(BaseModel):
    endpoint_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now())
    status_code: Optional[int] = 0
    latency: Optional[float] = None
    success: bool = False
    error: Optional[str] = None


class Endpoint(BaseModel):
    url: AnyHttpUrl
    timeout: int = Field(default=2, ge=1, description="The maximum number of seconds to wait for a response before considering the request timed out")
    alert_threshold: int = Field(default=3, ge=1, description="The number of consecutive failed checks before triggering an alert")


    


