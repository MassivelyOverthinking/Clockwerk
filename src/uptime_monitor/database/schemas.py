#-------------------- Imports --------------------

import datetime
from datetime import datetime as dt
from datetime import timedelta

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

#-------------------- Database Schemas --------------------

class Base(DeclarativeBase):
    pass


class EndpointStatus(Base):
    __tablename__ = "endpoint_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    current_status: Mapped[str] = mapped_column(String(50))
    last_updated: Mapped[dt] = mapped_column(default_factory=dt.now(datetime.timezone(offset=timedelta(0))))


class MonitorHistory(Base):
    __tablename__ = "monitor_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    timestamp: Mapped[dt] = mapped_column(default_factory=dt.now(datetime.timezone(offset=timedelta(0))))
    status_code: Mapped[int] = mapped_column(default="OK")
    latency: Mapped[float]
    success: Mapped[bool] = mapped_column(default=True)
    error: Mapped[str] = mapped_column(String(255))




