import pytest
from app.services.skill_gap_service import skill_gap_service
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_skill_gap_formula():
    """Verify formula: gap = max(target_mastery - current_mastery, 0)."""
    res = await skill_gap_service.calculate_user_skill_gaps("usr_demo")
    assert res is not None
    assert res.learning_goal == "Cybersecurity Analyst"
    for item in res.skills:
        expected_gap = max(round(item.target_mastery - item.current_mastery, 1), 0.0)
        assert item.gap == expected_gap
        assert item.gap >= 0.0


@pytest.mark.asyncio
async def test_zero_gap_when_mastery_exceeds_target():
    """Verify zero gap when current mastery >= target mastery."""
    res = await skill_gap_service.calculate_user_skill_gaps("usr_demo")
    python_skill = next((s for s in res.skills if s.skill == "Python"), None)
    if python_skill and python_skill.current_mastery >= python_skill.target_mastery:
        assert python_skill.gap == 0.0
        assert python_skill.category == "STRONG"


@pytest.mark.asyncio
async def test_career_goal_skill_mapping():
    """Verify career goals map to accurate required skills."""
    sec_skills = skill_gap_service._get_target_skills_for_goal("Cybersecurity Analyst")
    sec_names = [s["skill_name"] for s in sec_skills]
    assert "Networking" in sec_names
    assert "Linux" in sec_names
    assert "Cybersecurity" in sec_names

    ai_skills = skill_gap_service._get_target_skills_for_goal("AI/ML Engineer")
    ai_names = [s["skill_name"] for s in ai_skills]
    assert "Machine Learning" in ai_names
    assert "Deep Learning" in ai_names


@pytest.mark.asyncio
async def test_priority_calculation_and_categories():
    """Verify transparent priority calculation and category thresholds."""
    res = await skill_gap_service.calculate_user_skill_gaps("usr_demo")
    for item in res.skills:
        assert 0.0 <= item.priority <= 1.0
        assert item.category in ["STRONG", "DEVELOPING", "NEEDS_IMPROVEMENT", "CRITICAL_GAP"]
        assert item.priority_level in ["High", "Medium", "Low"]


def test_authentication_required_for_skill_gaps(client):
    """Verify 401 Unauthorized when requesting skill gaps without JWT."""
    response = client.get("/api/v1/skill-gaps")
    assert response.status_code == 401


def test_jwt_user_derivation_and_gap_response(client):
    """Verify skill gaps endpoint derives user from valid JWT token."""
    token = create_access_token(subject="usr_demo")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/skill-gaps", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_demo"
    assert "skills" in data
    assert len(data["skills"]) > 0


def test_skill_gap_detail_endpoint(client):
    """Verify skill gap detail endpoint returns specific skill data & explanations."""
    token = create_access_token(subject="usr_demo")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/skill-gaps/Networking", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["skill_name"] == "Networking"
    assert "explanation" in data
    assert "related_courses" in data
    assert len(data["related_courses"]) > 0


def test_explainable_recommendations_integration(client):
    """Verify recommendations engine returns data-driven explainable reasons."""
    response = client.post(
        "/api/v1/recommendations/personalized",
        json={"user_id": "usr_demo", "limit": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0

    first_rec = data["recommendations"][0]
    assert "recommendation_reason" in first_rec
    assert len(first_rec["recommendation_reason"]) > 10
    assert "target_skill_gap" in first_rec
    assert "gap" in first_rec
    assert "current_skill_level" in first_rec
    assert "target_skill_level" in first_rec
