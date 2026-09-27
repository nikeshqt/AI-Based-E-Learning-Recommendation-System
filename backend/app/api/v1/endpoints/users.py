from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.schemas.user import UserResponse
from app.services.user_service import user_service
from app.core.security import get_current_user_id


class UpdateGoalRequest(BaseModel):
    learning_goal: str


class SkillInputSchema(BaseModel):
    skill_name: str
    mastery_score: float  # 0.0 to 1.0
    category: Optional[str] = "Domain Skill"


class ProfileUpdateRequest(BaseModel):
    learning_goal: Optional[str] = None
    skills: Optional[List[SkillInputSchema]] = None
    interests: Optional[List[str]] = None


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user_id: str = Depends(get_current_user_id)):
    """Retrieve authenticated learner profile."""
    profile = await user_service.get_by_id(current_user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile


@router.put("/me/profile", response_model=UserResponse)
async def update_my_profile(
    body: ProfileUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    """Update authenticated learner target career goal, skills, and interests."""
    skills_dict_list = [s.model_dump() for s in body.skills] if body.skills else None
    updated = await user_service.update_user_profile(
        user_id=current_user_id,
        learning_goal=body.learning_goal,
        skills=skills_dict_list,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: str):
    """Retrieve learner profile by user ID."""
    profile = await user_service.get_by_id(user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile


@router.put("/{user_id}/goal", response_model=UserResponse)
async def update_user_goal(
    user_id: str,
    body: UpdateGoalRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    """Update learner target goal."""
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    updated = await user_service.update_learning_goal(user_id, body.learning_goal)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_profile(
    user_id: str,
    body: ProfileUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    """Update learner target career goal, skills, and interests."""
    if user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    skills_dict_list = [s.model_dump() for s in body.skills] if body.skills else None
    updated = await user_service.update_user_profile(
        user_id=user_id,
        learning_goal=body.learning_goal,
        skills=skills_dict_list,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated
