from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class EnrollmentModel(Base):
    """Course Enrollment stored in PostgreSQL enrollments table."""

    __tablename__ = "enrollments"

    enrollment_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="ENROLLED")  # ENROLLED, IN_PROGRESS, COMPLETED
    progress_percentage = Column(Float, default=0.0)
    enrolled_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("UserModel", back_populates="enrollments")
    course = relationship("CourseModel", back_populates="enrollments")


class ProgressModel(Base):
    """Lesson completion state stored in PostgreSQL progress table."""

    __tablename__ = "progress"

    progress_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    last_watched_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class AssessmentModel(Base):
    """Assessment / Quiz definition stored in PostgreSQL assessments table."""

    __tablename__ = "assessments"

    assessment_id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    max_score = Column(Float, default=1.0)


class QuizResultModel(Base):
    """Quiz Submission score stored in PostgreSQL quiz_results table."""

    __tablename__ = "quiz_results"

    result_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(String, ForeignKey("assessments.assessment_id"), nullable=False)
    score = Column(Float, nullable=False)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="quiz_results")
