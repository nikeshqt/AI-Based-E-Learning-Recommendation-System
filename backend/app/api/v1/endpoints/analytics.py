from fastapi import APIRouter

router = APIRouter()


@router.get("/user/{user_id}")
async def get_user_analytics(user_id: str):
    """Retrieve skill mastery breakdown and RecSys feedback analytics."""
    return {
        "user_id": user_id,
        "total_learning_time_minutes": 2550,
        "courses_completed": 4,
        "quizzes_passed": 18,
        "avg_quiz_score": 0.884,
        "monthly_progress": [
            {"month": "July", "hours_spent": 12.0, "skills_acquired": 2},
            {"month": "August", "hours_spent": 18.5, "skills_acquired": 3},
            {"month": "September", "hours_spent": 24.0, "skills_acquired": 4},
        ],
        "skill_breakdown": [
            {"skill_name": "Python", "proficiency_percentage": 85},
            {"skill_name": "Data Structs", "proficiency_percentage": 75},
            {"skill_name": "Machine Learning", "proficiency_percentage": 60},
            {"skill_name": "RecSys Architecture", "proficiency_percentage": 70},
        ],
    }
