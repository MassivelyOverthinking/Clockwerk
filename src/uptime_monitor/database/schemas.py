#-------------------- Imports --------------------

from datetime import datetime, timedelta, timezone

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
    last_updated: Mapped[datetime] = mapped_column(default_factory=lambda: datetime.now(timezone.utc))


class MonitorHistory(Base):
    __tablename__ = "monitor_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default_factory=lambda: datetime.now(timezone.utc))
    status_code: Mapped[int]
    latency: Mapped[float]
    success: Mapped[bool] = mapped_column(default=True)
    error: Mapped[str] = mapped_column(String(255))




