#-------------------- Imports --------------------

from typing import Optional, Literal, List
from enum import Enum
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.uptime_monitor.models import Endpoint

#-------------------- Config Models --------------------

class LoggerConfig(BaseModel):
    """
    Summary:
        Configuration model allowing for dynamic logging setup and handling.
     
    Attributes:
        log_level (Literal[str]): Defaults to 'INFO'.
        log_file (str): File path for the specified logging file. Default to 'Monitor.log'.
        log_to_fiel (bool): Determines whether to enable logging information to a file. Defaults to True.
        log_format (str): ASCII formatted string determining the logging information format.
        date_format (str): Used to determine how the logging module handles date formats.
    """
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = Field(default="monitor.log")
    log_to_file: bool = Field(default=True)
    log_format: str = Field(default="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")


class EmailConfig(BaseModel):
    """
    Summary:
    
    Attributes:
        smtp_host (str):
        smtp_port (int):
        email_from (EmailStr):
        email_to (EmailStr):
    """
    smtp_host: str = Field(default="smtp.mailtrap.io")
    smtp_port: int = Field(default=587, ge=1, le=65535)
    email_from: EmailStr
    email_to: EmailStr


class MonitorConfig(BaseModel):
    """
    Summary:
    
    Attributes:
        endpoints (List[Ednpoint]):
        check_interval (int):
        latency_threshold (float):
    """
    endpoints: List[Endpoint] = Field(default_factory=list)
    check_interval: int = Field(default=60, ge=5, description="Interval between Uptime checks")
    latency_threshold: float = Field(default=1.5, ge=0.5, description="Max acceptable latency in seconds")
    

class SupportedDrivers(str, Enum):
    """
    Summary:
        Database drivers currently supported for connectivity and querying (ENUM).
    
    Enums:
        mysql: Determines the appropriate driver string for MySQL database.
        postgresql: Determines the appropriate driver string for Postgresql database.
        sqlite: Determines the appropriate driver string for SQLite database.
    """
    mysql = "mysql+mysqlconnector"
    postgresql = "postgresql+asyncpg"
    sqlite = "sqlite+aiosqlite"


class DatabaseConfig(BaseModel):
    """
    Summary:
        Configuration model used to dynamically establish database connections. 

    Attributes:
        driver_name (SuppertedDrivers): The specified database driver used to establish initial connection.
        db_host_name (Optional[str]): Optinonal host name indetifying the desired database currently utilised.
        db_username (Optional[str]): Username associated with the appropriate database, allowing access to its functionalities.
        db_name (Optional[str]): The current identifying name userd by the database.
        db_password (Optional[str]): Optional password-string used to grant safe access to database functionalities.
        db_port (Optional[int]): Integer variable identifying the current port number used by the database. Defaults to 5437.
        db_activation (bool): Determine whether or not to enable database querying and information storage.
        echo_mode (bool): Whether or not current database enables 'Echo', a debugging tool. 
    """
    driver_name: SupportedDrivers
    db_host_name: Optional[str] = None
    db_username: Optional[str] = None
    db_name: Optional[str] = None
    db_password: Optional[str] = None
    db_port: Optional[int] = 5437
    db_activation: bool = False
    echo_mode: bool = False