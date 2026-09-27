from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


class SkillMasterySchema(BaseModel):
    skill_id: str
    skill_name: str
    mastery_score: float  # 0.0 to 1.0
    last_evaluated: datetime
    category: str


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    learning_goal: str
    preferred_learning_style: str = "visual"
    skill_level: str = "beginner"


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: str
    skills: List[SkillMasterySchema] = []
    weekly_goal_hours: int = 5
    completed_hours: float = 0.0
    streak_days: int = 0

    model_config = ConfigDict(from_attributes=True)
