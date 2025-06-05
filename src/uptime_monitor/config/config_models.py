#-------------------- Imports --------------------

from typing import Optional, Literal, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.uptime_monitor.models import Endpoint

#-------------------- Config Models --------------------

class LoggerConfig(BaseModel):
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = Field(default="monitor.log")
    log_to_file: bool = Field(default=True)
    log_format: str = Field(default="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")


class EmailConfig(BaseModel):
    smtp_host: str = Field(default="smtp.mailtrap.io")
    smtp_port: int = Field(default=587, ge=1, le=65535)
    email_from: EmailStr
    email_to: EmailStr


class MonitorConfig(BaseModel):
    endpoints: List[Endpoint] = Field(default_factory=list)
    check_interval: int = Field(default=60, ge=5, description="Interval between Uptime checks")
    latency_threshold: float = Field(default=1.5, ge=0.5, description="Max acceptable latency in seconds")
    

class SupportedDrivers(str, Enum):
    mysql = "mysql+mysqlconnector"
    postgresql = "postgresql+asyncpg"
    sqlite = "sqlite+aiosqlite"


class DatabaseConfig(BaseModel):
    driver_name: SupportedDrivers
    db_host_name: Optional[str] = None
    db_username: Optional[str] = None
    db_name: Optional[str] = None
    db_password: Optional[str] = None
    db_port: Optional[int] = 5437
    db_activation: bool = False
    echo_mode: bool = False