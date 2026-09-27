import pytest
from app.services.learning_path_service import learning_path_service
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_learning_path_generation_service():
    """Verify learning path generation service constructs ordered stages & transparent priority scores."""
    res = await learning_path_service.generate_learning_path(
        user_id="usr_demo", target_goal="Cybersecurity Analyst"
    )
    assert res is not None
    assert res.career_goal == "Cybersecurity Analyst"
    assert res.total_stages > 0
    assert res.total_courses > 0
    assert res.total_duration_hours > 0
    assert res.is_active is True

    # Verify stage ordering and courses
    for stage in res.stages:
        assert stage.stage_number in [1, 2, 3]
        assert len(stage.courses) > 0
        for item in stage.courses:
            assert item.priority_score > 0.0
            assert len(item.reason) > 10
            assert item.estimated_duration_hours > 0


@pytest.mark.asyncio
async def test_prerequisite_ordering_logic():
    """Verify prerequisite-aware ordering ensures foundational prerequisites precede advanced courses."""
    res = await learning_path_service.generate_learning_path(
        user_id="usr_demo", target_goal="Cybersecurity Analyst"
    )
    all_items = res.ordered_courses
    course_order_map = {item.course_title: idx for idx, item in enumerate(all_items)}

    # If both Linux and Advanced Security Analysis exist, Linux must come first
    linux_item = next((item for item in all_items if "Linux" in item.course_title), None)
    adv_sec_item = next((item for item in all_items if "Advanced Cybersecurity" in item.course_title), None)

    if linux_item and adv_sec_item:
        assert course_order_map[linux_item.course_title] < course_order_map[adv_sec_item.course_title]


@pytest.mark.asyncio
async def test_regeneration_deactivates_previous_active_path():
    """Verify generating a new path marks previous user paths as inactive."""
    res1 = await learning_path_service.generate_learning_path(user_id="usr_demo")
    res2 = await learning_path_service.generate_learning_path(user_id="usr_demo")

    assert res1.learning_path_id != res2.learning_path_id
    assert res2.is_active is True

    active_now = await learning_path_service.get_active_path_for_user(user_id="usr_demo")
    assert active_now.learning_path_id == res2.learning_path_id


def test_authentication_required_for_learning_paths(client):
    """Verify 401 Unauthorized when requesting learning paths without JWT."""
    response = client.get("/api/v1/learning-paths/current")
    assert response.status_code == 401

    response_gen = client.post("/api/v1/learning-paths/generate", json={})
    assert response_gen.status_code == 401


def test_jwt_learning_path_endpoints(client):
    """Verify generating and fetching learning path using valid JWT token."""
    token = create_access_token(subject="usr_demo")
    headers = {"Authorization": f"Bearer {token}"}

    # Generate path
    res_gen = client.post("/api/v1/learning-paths/generate", json={"target_goal": "Cybersecurity Analyst"}, headers=headers)
    assert res_gen.status_code == 200
    data_gen = res_gen.json()
    assert data_gen["user_id"] == "usr_demo"
    assert data_gen["career_goal"] == "Cybersecurity Analyst"

    # Fetch current active path
    res_curr = client.get("/api/v1/learning-paths/current", headers=headers)
    assert res_curr.status_code == 200
    data_curr = res_curr.json()
    assert data_curr["learning_path_id"] == data_gen["learning_path_id"]


def test_cross_user_isolation_ownership_enforcement(client):
    """Verify student cannot access another student's learning path (403 Forbidden)."""
    token_user_a = create_access_token(subject="usr_student_a")
    headers_a = {"Authorization": f"Bearer {token_user_a}"}

    # User A generates path
    res_a = client.post("/api/v1/learning-paths/generate", json={}, headers=headers_a)
    assert res_a.status_code == 200
    path_id_a = res_a.json()["learning_path_id"]

    # User B attempts to access User A's path_id
    token_user_b = create_access_token(subject="usr_student_b")
    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    res_b_attempt = client.get(f"/api/v1/learning-paths/{path_id_a}", headers=headers_b)
    assert res_b_attempt.status_code == 403
    assert "Forbidden" in res_b_attempt.json()["detail"]
