from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from datetime import datetime, timezone
from app.core.database import Base


class AnalyticsEventModel(Base):
    """Telemetry events stored in PostgreSQL analytics_events table."""

    __tablename__ = "analytics_events"

    event_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String, index=True, nullable=False)
    payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
