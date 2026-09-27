from fastapi import APIRouter, status, Depends
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.event import InteractionEventSchema
from app.services.recsys_service import recsys_service
from app.core.security import get_current_user_id
import uuid

router = APIRouter()


@router.get("/personalized", response_model=RecommendationResponse)
async def get_my_personalized_recommendations(
    limit: int = 10,
    current_user_id: str = Depends(get_current_user_id),
):
    """Run RecSys pipeline for authenticated student."""
    return await recsys_service.get_personalized_recommendations(current_user_id, limit)


@router.post("/personalized", response_model=RecommendationResponse)
async def get_personalized_recommendations(req: RecommendationRequest):
    """Run RecSys pipeline and return personalized recommendations for a specified user."""
    return await recsys_service.get_personalized_recommendations(req.user_id, req.limit)


@router.post("/events/track", status_code=status.HTTP_202_ACCEPTED)
async def track_event(event: InteractionEventSchema):
    """Real-time micro-interaction telemetry event ingestion."""
    event_id = event.event_id or f"evt_{uuid.uuid4().hex[:8]}"
    return {
        "status": "ingested",
        "event_id": event_id,
        "user_id": event.user_id,
        "processed_by": "KafkaEventInletStub",
    }

