from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class SkillModel(Base):
    """Skill taxonomy entity stored in PostgreSQL skills table."""

    __tablename__ = "skills"

    skill_id = Column(String, primary_key=True, index=True)
    skill_name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user_skills = relationship("UserSkillModel", back_populates="skill")
    course_skills = relationship("CourseSkillModel", back_populates="skill")


class UserSkillModel(Base):
    """Learner skill vector evaluation stored in PostgreSQL user_skills table."""

    __tablename__ = "user_skills"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(String, ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False)
    mastery_score = Column(Float, default=0.0)
    last_evaluated = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="skills")
    skill = relationship("SkillModel", back_populates="user_skills")


class GoalRequiredSkillModel(Base):
    """Career Goal to required skills and target mastery thresholds stored in PostgreSQL goal_required_skills table."""

    __tablename__ = "goal_required_skills"

    id = Column(String, primary_key=True, index=True)
    goal_name = Column(String, index=True, nullable=False)
    skill_name = Column(String, index=True, nullable=False)
    target_mastery = Column(Float, nullable=False)  # 0.0 to 1.0 or 0 to 100
    importance = Column(Float, default=1.0)
    is_prerequisite = Column(Boolean, default=False)
