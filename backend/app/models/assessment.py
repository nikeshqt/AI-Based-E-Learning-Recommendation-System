from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base


class AssessmentQuestionModel(Base):
    """Technical Question definition stored in PostgreSQL assessment_questions table."""

    __tablename__ = "assessment_questions"

    question_id = Column(String, primary_key=True, index=True)
    assessment_id = Column(String, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False, index=True)
    domain = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False)  # BEGINNER, INTERMEDIATE, ADVANCED
    prompt = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=True)
    options = Column(JSON, nullable=False)  # List of 4 option strings
    correct_answer = Column(String, nullable=False)  # Correct option text or index
    explanation = Column(Text, nullable=False)
    skill_measured = Column(String, nullable=False, index=True)


class AssessmentAttemptModel(Base):
    """Assessment Submission Attempt stored in PostgreSQL assessment_attempts table."""

    __tablename__ = "assessment_attempts"

    attempt_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(String, ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False)
    total_questions = Column(Integer, nullable=False)
    answered_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    incorrect_answers = Column(Integer, nullable=False)
    overall_score = Column(Float, nullable=False)  # 0.0 - 100.0
    topic_scores = Column(JSON, nullable=False)  # Dict[domain, score_pct]
    difficulty_performance = Column(JSON, nullable=False)  # Dict[BEGINNER/INTERMEDIATE/ADVANCED, pct]
    skill_proficiency = Column(JSON, nullable=False)  # Dict[skill, proficiency_label]
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("UserModel", back_populates="assessment_attempts")
    answers = relationship("AssessmentAnswerModel", back_populates="attempt", cascade="all, delete-orphan")


class AssessmentAnswerModel(Base):
    """Submitted Question Answer stored in PostgreSQL assessment_answers table."""

    __tablename__ = "assessment_answers"

    answer_id = Column(String, primary_key=True, index=True)
    attempt_id = Column(String, ForeignKey("assessment_attempts.attempt_id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String, ForeignKey("assessment_questions.question_id", ondelete="CASCADE"), nullable=False)
    selected_option = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    attempt = relationship("AssessmentAttemptModel", back_populates="answers")
