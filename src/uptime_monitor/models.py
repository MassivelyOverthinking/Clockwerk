#-------------------- Imports --------------------

from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr, AnyHttpUrl


#-------------------- Monitor Result --------------------

@dataclass
class MonitorResult:
    endpoint_name: str = None
    timestamp: datetime = field(default_factory=datetime.now())
    status_code: int = None
    latency: float = None
    success: bool = False
    error: str = None

class Endpoint(BaseModel):
    url: AnyHttpUrl
    timeout: int = Field(default=2, ge=1, description="The maximum number of seconds to wait for a response before considering the request timed out")
    alert_threshold: int = Field(default=3, ge=1, description="The number of consecutive failed checks before triggering an alert")


class LoggerConfig(BaseModel):
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="monitor.log")
    log_to_file: bool = Field(default=True)
    log_format: str = Field(default="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")

    @field_validator("log_level")
    def validate_log_level(cls, v):
        validations_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v not in validations_levels:
            raise ValueError(f"Invalid log level: {v}")
        return v


class EmailConfig(BaseModel):
    smtp_host: str = Field(default="smtp.mailtrap.io")
    smtp_port: int = Field(default=587, ge=1, le=65535)
    email_from: EmailStr
    email_to: EmailStr


class MonitorConfig(BaseModel):
    endpoints: List[Endpoint]
    check_interval: int = Field(default=60, ge=5, description="Interval between Uptime checks")
    latency_threshold: float = Field(default=1.5, ge=0.5, description="Max acceptable latency in seconds")


