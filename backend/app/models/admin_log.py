from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class AdminActivityLogModel(Base):
    """Administrative action audit trail stored in PostgreSQL admin_activity_logs table."""

    __tablename__ = "admin_activity_logs"

    log_id = Column(String, primary_key=True, index=True)
    admin_id = Column(String, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String, nullable=False, index=True)
    target_type = Column(String, nullable=True, index=True)  # e.g., 'student', 'course', 'progress', 'auth'
    target_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)  # Contextual description (no passwords or credentials)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    admin = relationship("UserModel")
