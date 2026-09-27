from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class UserModel(Base):
    """User account entity stored in PostgreSQL users table."""

    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    profile = relationship("ProfileModel", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skills = relationship("UserSkillModel", back_populates="user", cascade="all, delete-orphan")
    enrollments = relationship("EnrollmentModel", back_populates="user", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResultModel", back_populates="user", cascade="all, delete-orphan")
    assessment_attempts = relationship("AssessmentAttemptModel", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("RecommendationModel", back_populates="user", cascade="all, delete-orphan")
    learning_paths = relationship("LearningPathModel", back_populates="user", cascade="all, delete-orphan")


class ProfileModel(Base):
    """Learner profile preferences stored in PostgreSQL profiles table."""

    __tablename__ = "profiles"

    profile_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    learning_goal = Column(String, nullable=False)
    preferred_learning_style = Column(String, default="visual")
    skill_level = Column(String, default="beginner")
    weekly_goal_hours = Column(Integer, default=5)
    completed_hours = Column(Float, default=0.0)
    streak_days = Column(Integer, default=0)

    user = relationship("UserModel", back_populates="profile")
