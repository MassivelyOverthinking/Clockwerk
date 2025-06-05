from typing import Optional
from typing import List
from pydantic import BaseModel, Field, field_validator, EmailStr
from src.uptime_monitor.models import Endpoint

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


class DatabaseConfig(BaseModel):
    driver_name: str
    db_host_name: Optional[str] = None
    db_username: Optional[str] = None
    db_name: Optional[str] = None
    db_password: Optional[str] = None
    db_port: Optional[int] = 5437
    db_activation: bool = False
    echo_mode: bool = False

    @field_validator("driver_name")
    def validate_driver(cls, v: str):
        drivers = {
            "mysql": "mysql+mysqlconnector",
            "postgresql": "postgresql+asyncpg",
            "sqlite": "sqlite+aiosqlite"
        }
        if v.lower() not in drivers:
            raise ValueError(f"Invalid database driver! {v}. Must be one of {list(drivers)}")
        return drivers[v.lower()]