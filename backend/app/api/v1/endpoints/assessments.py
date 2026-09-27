from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.assessment import (
    AssessmentSchema,
    QuestionPublicSchema,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    AssessmentAttemptHistoryResponse,
)
from app.services.assessment_service import assessment_service
from app.core.security import get_current_user_id

router = APIRouter()


@router.get("", response_model=List[AssessmentSchema])
@router.get("/", response_model=List[AssessmentSchema])
async def list_assessments():
    """Retrieve available technical skill assessments."""
    return await assessment_service.get_available_assessments()


@router.get("/history", response_model=AssessmentAttemptHistoryResponse)
async def get_assessment_history(
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve assessment submission history for authenticated student."""
    return await assessment_service.get_user_history(user_id=current_user_id)


@router.get("/{assessment_id}/questions", response_model=List[QuestionPublicSchema])
async def get_assessment_questions(
    assessment_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve assessment questions for authenticated student (answer key hidden)."""
    questions = await assessment_service.get_questions_for_student(assessment_id)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment questions not found")
    return questions


@router.post("/{assessment_id}/submit", response_model=AssessmentResultResponse)
async def submit_assessment(
    assessment_id: str,
    body: AssessmentSubmitRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    """Submit student assessment answers, evaluate scoring, update skills, and persist attempt."""
    result = await assessment_service.submit_assessment(
        user_id=current_user_id,
        assessment_id=assessment_id,
        payload=body,
    )
    return result


@router.get("/{assessment_id}/results", response_model=AssessmentResultResponse)
async def get_latest_assessment_result(
    assessment_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Retrieve latest assessment result for authenticated student (enforces authorization)."""
    result = await assessment_service.get_latest_user_result(
        user_id=current_user_id,
        assessment_id=assessment_id,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment submission result found for this user",
        )
    return result
