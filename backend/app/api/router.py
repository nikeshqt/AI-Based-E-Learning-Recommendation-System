from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    users,
    catalog,
    recommendations,
    learning_paths,
    analytics,
    assessments,
    skill_gaps,
    course_learning,
    ai_tutor,
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["Course Catalog"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Skill Assessments"])
api_router.include_router(skill_gaps.router, prefix="/skill-gaps", tags=["Skill Gap Analysis"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["Recommendation Engine"]
)
api_router.include_router(
    learning_paths.router, prefix="/learning-paths", tags=["Adaptive Pathways"]
)
api_router.include_router(course_learning.router, tags=["Course Learning"])
api_router.include_router(ai_tutor.router, prefix="/ai-tutor", tags=["AI Tutor"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])



