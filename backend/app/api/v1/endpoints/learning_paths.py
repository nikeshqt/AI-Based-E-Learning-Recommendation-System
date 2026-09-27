from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from app.schemas.learning_path import (
    LearningPathResponse,
    LearningPathGenerateRequest,
)
from app.services.learning_path_service import learning_path_service
from app.core.security import get_current_user_id

router = APIRouter()


@router.post("/generate", response_model=LearningPathResponse)
async def generate_learning_path(
    body: Optional[LearningPathGenerateRequest] = None,
    current_user_id: str = Depends(get_current_user_id),
):
    """Generate a personalized prerequisite-aware learning path for the authenticated student."""
    target_goal = body.target_goal if body else None
    return await learning_path_service.generate_learning_path(
        user_id=current_user_id,
        target_goal=target_goal,
    )


@router.get("/current", response_model=LearningPathResponse)
async def get_current_learning_path(
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve the current active personalized learning path for the authenticated student."""
    path = await learning_path_service.get_active_path_for_user(user_id=current_user_id)
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active learning path found for this user.",
        )
    return path


@router.get("/{learning_path_id}", response_model=LearningPathResponse)
async def get_learning_path_details(
    learning_path_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve details for a specific learning path (enforces user ownership authorization)."""
    path, is_authorized = await learning_path_service.get_path_by_id(
        path_id=learning_path_id,
        current_user_id=current_user_id,
    )
    if not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not have permission to access this learning path.",
        )
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Learning path '{learning_path_id}' not found.",
        )
    return path
