import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_course_enrollment_and_learning_flow():
    """Test course enrollment, fetching modules/lessons, completing lessons, and tracking progress percentage."""
    unique_user_id = f"usr_test_{uuid.uuid4().hex[:6]}"
    token = create_access_token(subject=unique_user_id)
    auth_headers = {"Authorization": f"Bearer {token}"}
    course_id = "crs_sec_04"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Enroll in course
        enroll_res = await ac.post(
            f"/api/v1/courses/{course_id}/enroll", headers=auth_headers
        )
        assert enroll_res.status_code == 200
        enroll_data = enroll_res.json()
        assert enroll_data["course_id"] == course_id
        assert enroll_data["status"] in ["ENROLLED", "IN_PROGRESS"]
        assert enroll_data["progress_percentage"] == 0.0

        # 2. Fetch learning content
        content_res = await ac.get(
            f"/api/v1/courses/{course_id}/learning", headers=auth_headers
        )
        assert content_res.status_code == 200
        content_data = content_res.json()
        assert content_data["course_id"] == course_id
        assert len(content_data["modules"]) > 0
        first_module = content_data["modules"][0]
        assert len(first_module["lessons"]) > 0
        first_lesson = first_module["lessons"][0]

        # 3. Complete first lesson
        lesson_id = first_lesson["lesson_id"]
        complete_res = await ac.post(
            f"/api/v1/courses/{course_id}/lessons/{lesson_id}/complete",
            headers=auth_headers,
        )
        assert complete_res.status_code == 200
        complete_data = complete_res.json()
        assert complete_data["lesson_id"] == lesson_id
        assert complete_data["is_completed"] is True
        assert complete_data["progress_percentage"] > 0.0

        # 4. Check continue learning endpoint
        cont_res = await ac.get("/api/v1/learning/continue", headers=auth_headers)
        assert cont_res.status_code == 200
        cont_data = cont_res.json()
        assert cont_data["has_active_course"] is True
        assert cont_data["course_id"] == course_id

        # 5. Check dashboard stats
        stats_res = await ac.get(
            "/api/v1/learning/dashboard-stats", headers=auth_headers
        )
        assert stats_res.status_code == 200
        stats_data = stats_res.json()
        assert stats_data["in_progress_courses_count"] >= 1


@pytest.mark.asyncio
async def test_course_learning_unauthorized():
    """Verify 401 Unauthorized for unauthenticated requests."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/learning/continue")
        assert res.status_code == 401
