from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.course import CourseResponse


class RecommendationRequest(BaseModel):
    user_id: str
    limit: int = 10
    preferred_category: Optional[str] = None
    max_duration_hours: Optional[float] = None


class RecommendationItemSchema(BaseModel):
    recommendation_id: str
    course: CourseResponse
    match_score: float  # 0.0 to 1.0
    recommendation_reason: str
    stage_sources: List[str]
    prerequisites_met: bool
    target_skill_gap: str
    matched_skills: Optional[List[str]] = None
    skill_gaps_addressed: Optional[List[str]] = None
    current_skill_level: Optional[float] = None  # Percentage 0 - 100
    target_skill_level: Optional[float] = None   # Percentage 0 - 100
    gap: Optional[float] = None                  # Percentage 0 - 100


class RecommendationResponse(BaseModel):
    user_id: str
    generated_at: datetime
    recommendations: List[RecommendationItemSchema]
