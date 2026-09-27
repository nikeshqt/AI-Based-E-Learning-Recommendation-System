from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class LearningPathGenerateRequest(BaseModel):
    """Optional request parameters for learning path generation."""

    target_goal: Optional[str] = None


class LearningPathItemSchema(BaseModel):
    """Schema representing an individual course item in the learning path."""

    model_config = ConfigDict(from_attributes=True)

    item_id: Optional[str] = None
    path_id: Optional[str] = None
    order_index: int
    stage_number: int
    stage_title: str
    stage_name: Optional[str] = None
    stage_description: Optional[str] = None
    course_id: str
    course_title: str
    target_skill: str
    skill_gap: float
    current_mastery: float
    target_mastery: float
    priority_score: float
    reason: str
    status: str = "AVAILABLE"  # AVAILABLE, LOCKED, IN_PROGRESS, COMPLETED
    estimated_duration_hours: float
    prerequisites: List[str] = []
    skills_taught: List[str] = []


class LearningPathStageSchema(BaseModel):
    """Schema representing a logical stage in the learning path."""

    stage_number: int
    stage_title: str
    stage_name: str
    description: str
    target_skills: List[str]
    estimated_duration_hours: float
    status: str = "AVAILABLE"
    courses: List[LearningPathItemSchema]


class LearningPathResponse(BaseModel):
    """Full personalized learning path response schema."""

    model_config = ConfigDict(from_attributes=True)

    learning_path_id: str
    user_id: str
    career_goal: str
    overall_readiness: float
    total_duration_hours: float
    total_stages: int
    total_courses: int
    generated_at: datetime
    is_active: bool = True
    stages: List[LearningPathStageSchema]
    ordered_courses: List[LearningPathItemSchema]
