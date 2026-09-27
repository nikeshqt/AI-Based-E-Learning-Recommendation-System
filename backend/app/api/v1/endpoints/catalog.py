from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas.course import CourseResponse
from app.services.catalog_service import catalog_service

router = APIRouter()


@router.get("/courses", response_model=List[CourseResponse])
async def list_courses(category: Optional[str] = None):
    """Retrieve course catalog listing."""
    return await catalog_service.list_courses(category=category)


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course_details(course_id: str):
    """Retrieve detailed course information and video lessons."""
    course = await catalog_service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course
