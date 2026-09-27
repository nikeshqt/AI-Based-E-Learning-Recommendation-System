from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class RecommendationModel(Base):
    """Personalized recommendations stored in PostgreSQL recommendations table."""

    __tablename__ = "recommendations"

    recommendation_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="recommendations")


class LearningPathModel(Base):
    """Adaptive Learning Path stored in PostgreSQL learning_paths table."""

    __tablename__ = "learning_paths"

    path_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    overall_goal = Column(String, nullable=False)
    total_duration_weeks = Column(Integer, default=12)
    is_active = Column(Boolean, default=True, index=True)
    overall_readiness = Column(Float, default=0.0)
    total_duration_hours = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="learning_paths")
    items = relationship(
        "LearningPathItemModel",
        back_populates="path",
        cascade="all, delete-orphan",
        order_by="LearningPathItemModel.order_index",
    )


class LearningPathItemModel(Base):
    """Stages & courses in roadmap stored in PostgreSQL learning_path_items table."""

    __tablename__ = "learning_path_items"

    item_id = Column(String, primary_key=True, index=True)
    path_id = Column(String, ForeignKey("learning_paths.path_id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=1)
    stage_number = Column(Integer, nullable=False)
    stage_title = Column(String, nullable=False)
    stage_name = Column(String, nullable=True)
    stage_description = Column(Text, nullable=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    target_skill = Column(String, nullable=True)
    skill_gap = Column(Float, default=0.0)
    current_mastery = Column(Float, default=0.0)
    target_mastery = Column(Float, default=0.0)
    priority_score = Column(Float, default=0.0)
    reason = Column(Text, nullable=True)
    status = Column(String, default="AVAILABLE")
    estimated_weeks = Column(Integer, default=3)
    estimated_duration_hours = Column(Float, default=0.0)

    path = relationship("LearningPathModel", back_populates="items")
    course = relationship("CourseModel")

