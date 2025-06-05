#-------------------- Imports --------------------

from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

#-------------------- Database Schemas --------------------

class Base(DeclarativeBase):
    pass


class EndpointStatus(Base):
    __tablename__ = "endpoint_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2083), unique=True, nullable=False)
    current_status: Mapped[str] = mapped_column(String(50), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(default_factory=lambda: datetime.now(timezone.utc))


class MonitorHistory(Base):
    __tablename__ = "monitor_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2083), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default_factory=lambda: datetime.now(timezone.utc))
    status_code: Mapped[int] = mapped_column(nullable=False)
    latency: Mapped[float] = mapped_column(nullable=False)
    success: Mapped[bool] = mapped_column(default=True)
    error: Mapped[str] = mapped_column(String(255), nullable=True)




