from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.learning_progress import (
    EnrollmentResponse,
    CourseLearningResponse,
    LessonCompleteResponse,
    ContinueLearningResponse,
    DashboardStatsResponse,
)
from app.services.learning_progress_service import learning_progress_service
from app.core.security import get_current_user_id

router = APIRouter()


@router.post("/courses/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_in_course(
    course_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Enroll authenticated student in a course."""
    return await learning_progress_service.enroll_user(
        user_id=current_user_id,
        course_id=course_id,
    )


@router.get("/courses/{course_id}/learning", response_model=CourseLearningResponse)
async def get_course_learning_content(
    course_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve modules, lessons, and completion status for a course."""
    return await learning_progress_service.get_course_learning_content(
        user_id=current_user_id,
        course_id=course_id,
    )


@router.post(
    "/courses/{course_id}/lessons/{lesson_id}/complete",
    response_model=LessonCompleteResponse,
)
async def complete_lesson(
    course_id: str,
    lesson_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Mark a lesson complete and update overall course progress percentage."""
    return await learning_progress_service.complete_lesson(
        user_id=current_user_id,
        course_id=course_id,
        lesson_id=lesson_id,
    )


@router.get("/learning/continue", response_model=ContinueLearningResponse)
async def get_continue_learning(
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve active course and next incomplete lesson for authenticated student."""
    return await learning_progress_service.get_continue_learning(
        user_id=current_user_id,
    )


@router.get("/learning/dashboard-stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve completed/in-progress course counts & active continue learning payload."""
    return await learning_progress_service.get_dashboard_stats(
        user_id=current_user_id,
    )
