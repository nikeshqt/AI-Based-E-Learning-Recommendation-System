from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class EnrollmentResponse(BaseModel):
    """Enrollment record response schema."""

    model_config = ConfigDict(from_attributes=True)

    enrollment_id: str
    user_id: str
    course_id: str
    status: str  # ENROLLED, IN_PROGRESS, COMPLETED
    progress_percentage: float
    enrolled_at: datetime
    completed_at: Optional[datetime] = None


class LessonPublicSchema(BaseModel):
    """Schema representing individual lesson details and student completion status."""

    model_config = ConfigDict(from_attributes=True)

    lesson_id: str
    module_id: str
    course_id: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    order_index: int
    estimated_duration_minutes: int
    is_completed: bool = False


class ModulePublicSchema(BaseModel):
    """Schema representing module grouping with nested lessons."""

    model_config = ConfigDict(from_attributes=True)

    module_id: str
    course_id: str
    title: str
    order_index: int
    lessons: List[LessonPublicSchema]


class CourseLearningResponse(BaseModel):
    """Complete course learning content and progress schema."""

    model_config = ConfigDict(from_attributes=True)

    course_id: str
    title: str
    category: str
    difficulty_level: str
    duration_hours: float
    status: str
    progress_percentage: float
    completed_lessons_count: int
    total_lessons_count: int
    modules: List[ModulePublicSchema]


class LessonCompleteResponse(BaseModel):
    """Response returned when a student marks a lesson complete."""

    lesson_id: str
    course_id: str
    is_completed: bool = True
    progress_percentage: float
    course_completed: bool = False
    status: str


class ContinueLearningResponse(BaseModel):
    """Most relevant active course & next incomplete lesson for dashboard."""

    has_active_course: bool = False
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    progress_percentage: Optional[float] = 0.0
    next_lesson_id: Optional[str] = None
    next_lesson_title: Optional[str] = None
    estimated_duration_minutes: Optional[int] = 15


class DashboardStatsResponse(BaseModel):
    """Dashboard statistics and active continue learning payload."""

    completed_courses_count: int = 0
    in_progress_courses_count: int = 0
    continue_learning: Optional[ContinueLearningResponse] = None
