from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class SkillGapItemSchema(BaseModel):
    """Schema representing an individual skill gap evaluation for a career goal."""

    model_config = ConfigDict(from_attributes=True)

    skill: str
    skill_id: Optional[str] = None
    current_mastery: float  # Percentage 0 - 100
    target_mastery: float   # Percentage 0 - 100
    gap: float              # Percentage max(target - current, 0)
    priority: float         # Normalized 0.0 - 1.0
    priority_level: str     # "High", "Medium", "Low"
    category: str           # "STRONG", "DEVELOPING", "NEEDS_IMPROVEMENT", "CRITICAL_GAP"
    is_prerequisite: bool = False
    importance: float = 1.0


class SkillGapResponse(BaseModel):
    """Overall skill gap overview response for authenticated student."""

    model_config = ConfigDict(from_attributes=True)

    user_id: str
    learning_goal: str
    overall_readiness: float  # Percentage 0 - 100
    skills: List[SkillGapItemSchema]


class SkillGapDetailResponse(BaseModel):
    """Detailed skill gap analysis and related course mapping response."""

    model_config = ConfigDict(from_attributes=True)

    skill_name: str
    skill_id: Optional[str] = None
    current_mastery: float
    target_mastery: float
    gap: float
    proficiency: str
    priority: float
    priority_level: str
    category: str
    is_prerequisite: bool
    explanation: str
    related_courses: List[str]
    prerequisite_skills: List[str]
