from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Optional
from datetime import datetime


class AssessmentSchema(BaseModel):
    """Assessment metadata response schema."""

    model_config = ConfigDict(from_attributes=True)

    assessment_id: str
    course_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    total_questions: int = 40
    time_limit_minutes: int = 45


class QuestionPublicSchema(BaseModel):
    """Sanitized Question schema for student retrieval (hides correct_answer & explanation)."""

    model_config = ConfigDict(from_attributes=True)

    question_id: str
    assessment_id: str
    domain: str
    difficulty: str
    prompt: str
    code_snippet: Optional[str] = None
    options: List[str]
    skill_measured: str


class AnswerSubmissionSchema(BaseModel):
    """Single question answer submission payload."""

    question_id: str
    selected_option: str


class AssessmentSubmitRequest(BaseModel):
    """Payload for submitting assessment answers."""

    answers: List[AnswerSubmissionSchema]


class AssessmentResultResponse(BaseModel):
    """Calculated assessment performance and skill evaluation response."""

    model_config = ConfigDict(from_attributes=True)

    attempt_id: str
    assessment_id: str
    user_id: str
    total_questions: int
    answered_questions: int
    correct_answers: int
    incorrect_answers: int
    overall_score: float  # 0.0 - 100.0
    topic_scores: Dict[str, float]  # domain -> pct
    difficulty_performance: Dict[str, float]  # BEGINNER/INTERMEDIATE/ADVANCED -> pct
    skill_proficiency: Dict[str, str]  # skill -> label
    submitted_at: datetime


class AssessmentAttemptHistoryResponse(BaseModel):
    """Learner historical assessment attempts response."""

    user_id: str
    total_attempts: int
    attempts: List[AssessmentResultResponse]
