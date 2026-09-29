from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from app.core.security import get_current_admin
from app.services.admin_service import admin_service
from app.schemas.admin import (
    AdminDashboardStats,
    AdminStudentListResponse,
    AdminStudentDetailResponse,
    AdminStudentStatusUpdate,
    AdminCourseItem,
    AdminCourseCreate,
    AdminCourseUpdate,
    AdminCourseStatusUpdate,
    AdminProgressItem,
    AdminProgressUpdate,
    AdminAnalyticsResponse,
    AdminActivityItem,
)

router = APIRouter(dependencies=[Depends(get_current_admin)])


@router.get("/dashboard", response_model=AdminDashboardStats)
async def get_admin_dashboard(admin=Depends(get_current_admin)):
    """Retrieve high-level metrics, enrollment trends, and recent activities for the admin overview."""
    return await admin_service.get_dashboard_stats()


@router.get("/students", response_model=AdminStudentListResponse)
async def get_students_list(
    search: Optional[str] = Query(None, description="Search by student name or email"),
    career_goal: Optional[str] = Query(None, description="Filter by career goal"),
    assessment_status: Optional[str] = Query(None, description="Filter: completed or not_completed"),
    account_status: Optional[str] = Query(None, description="Filter: active or inactive"),
    sort_by: str = Query("created_at", description="Sort by: created_at, name, email, progress"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    admin=Depends(get_current_admin),
):
    """Retrieve student accounts with filtering, search, and aggregated completion stats."""
    return await admin_service.list_students(
        search=search,
        career_goal=career_goal,
        assessment_status=assessment_status,
        account_status=account_status,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/students/{student_id}", response_model=AdminStudentDetailResponse)
async def get_student_detail(student_id: str, admin=Depends(get_current_admin)):
    """Retrieve comprehensive 360-degree student profile including assessment, skill gaps, path, and progress."""
    detail = await admin_service.get_student_detail(student_id)
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student account '{student_id}' not found",
        )
    return detail


@router.patch("/students/{student_id}/status")
async def update_student_account_status(
    student_id: str,
    status_in: AdminStudentStatusUpdate,
    admin=Depends(get_current_admin),
):
    """Activate or deactivate student account with automated audit logging."""
    admin_id = getattr(admin, "user_id", str(admin))
    success = await admin_service.update_student_status(
        student_id=student_id,
        is_active=status_in.is_active,
        admin_id=admin_id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student account '{student_id}' not found",
        )
    return {
        "status": "success",
        "student_id": student_id,
        "is_active": status_in.is_active,
        "message": f"Student account {'activated' if status_in.is_active else 'deactivated'} successfully",
    }


@router.get("/courses", response_model=List[AdminCourseItem])
async def list_admin_courses(admin=Depends(get_current_admin)):
    """List all catalog courses with enrolled student counts, modules, and lessons."""
    return await admin_service.list_courses()


@router.post("/courses", response_model=AdminCourseItem, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: AdminCourseCreate,
    admin=Depends(get_current_admin),
):
    """Create a new course in catalog and register it with the RecSys engine."""
    admin_id = getattr(admin, "user_id", str(admin))
    return await admin_service.create_course(course_in, admin_id=admin_id)


@router.put("/courses/{course_id}", response_model=AdminCourseItem)
async def update_course(
    course_id: str,
    course_in: AdminCourseUpdate,
    admin=Depends(get_current_admin),
):
    """Update course attributes and synchronize with the recommendation engine."""
    admin_id = getattr(admin, "user_id", str(admin))
    updated = await admin_service.update_course(course_id, course_in, admin_id=admin_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course '{course_id}' not found",
        )
    return updated


@router.patch("/courses/{course_id}/status")
async def update_course_status(
    course_id: str,
    status_in: AdminCourseStatusUpdate,
    admin=Depends(get_current_admin),
):
    """Activate or deactivate a course."""
    admin_id = getattr(admin, "user_id", str(admin))
    success = await admin_service.update_course_status(
        course_id=course_id,
        is_active=status_in.is_active,
        admin_id=admin_id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course '{course_id}' not found",
        )
    return {
        "status": "success",
        "course_id": course_id,
        "is_active": status_in.is_active,
        "message": f"Course {'activated' if status_in.is_active else 'deactivated'} successfully",
    }


@router.get("/progress", response_model=List[AdminProgressItem])
async def list_course_progress(
    course_id: Optional[str] = Query(None, description="Filter by course ID"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
    status: Optional[str] = Query(None, description="Filter by status: ENROLLED, IN_PROGRESS, COMPLETED"),
    admin=Depends(get_current_admin),
):
    """Inspect student course progress records across courses and learners."""
    return await admin_service.list_progress_records(
        course_id=course_id,
        student_id=student_id,
        status=status,
    )


@router.patch("/progress/{enrollment_id}", response_model=AdminProgressItem)
async def update_progress_record(
    enrollment_id: str,
    update_in: AdminProgressUpdate,
    admin=Depends(get_current_admin),
):
    """Perform administrative progress correction with audit recording."""
    admin_id = getattr(admin, "user_id", str(admin))
    updated = await admin_service.update_progress_record(
        enrollment_id=enrollment_id,
        update_in=update_in,
        admin_id=admin_id,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment record '{enrollment_id}' not found",
        )
    return updated


@router.get("/analytics", response_model=AdminAnalyticsResponse)
async def get_system_analytics(admin=Depends(get_current_admin)):
    """Retrieve system-level analytics derived directly from real database records."""
    return await admin_service.get_system_analytics()


@router.get("/activity", response_model=List[AdminActivityItem])
async def get_recent_activity(
    limit: int = Query(50, ge=1, le=100),
    admin=Depends(get_current_admin),
):
    """Retrieve administrative action audit logs."""
    return await admin_service.get_activity_logs(limit=limit)
