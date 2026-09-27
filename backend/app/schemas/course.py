from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class LessonSchema(BaseModel):
    lesson_id: str
    title: str
    duration_minutes: int
    video_url: Optional[str] = None
    is_completed: bool = False


class CourseBase(BaseModel):
    title: str
    description: str
    instructor_name: str
    category: str
    difficulty_level: str
    duration_hours: float
    rating: float = 5.0
    prerequisites: List[str] = []
    skills_taught: List[str] = []


class CourseResponse(CourseBase):
    course_id: str
    thumbnail_url: Optional[str] = None
    enrolled_count: int = 0
    lessons: List[LessonSchema] = []

    model_config = ConfigDict(from_attributes=True)
