from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.skill_gap import SkillGapResponse, SkillGapDetailResponse
from app.services.skill_gap_service import skill_gap_service
from app.core.security import get_current_user_id

router = APIRouter()


@router.get("", response_model=SkillGapResponse)
@router.get("/", response_model=SkillGapResponse)
async def get_user_skill_gaps(
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve authenticated student's skill gap analysis for their current career goal."""
    return await skill_gap_service.calculate_user_skill_gaps(user_id=current_user_id)


@router.get("/{skill_id}", response_model=SkillGapDetailResponse)
async def get_skill_gap_detail(
    skill_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve detailed skill gap analysis and related courses for a specific skill."""
    detail = await skill_gap_service.get_skill_gap_detail(
        user_id=current_user_id,
        skill_id_or_name=skill_id,
    )
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill gap detail for '{skill_id}' not found.",
        )
    return detail
