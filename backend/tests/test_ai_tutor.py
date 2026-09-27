import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_ai_tutor_chat_authenticated():
    """Verify AI Tutor response with authenticated JWT token and lesson context."""
    token = create_access_token(subject="usr_demo")
    auth_headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Test explain simply action
        res = await ac.post(
            "/api/v1/ai-tutor/chat",
            headers=auth_headers,
            json={
                "message": "Explain this lesson simply.",
                "course_id": "crs_sec_04",
                "lesson_id": "lsn_sec_1",
                "action": "explain_simply",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "reply" in data
        assert len(data["reply"]) > 20
        assert "source_context" in data

        # Test quick action quiz_me
        quiz_res = await ac.post(
            "/api/v1/ai-tutor/chat",
            headers=auth_headers,
            json={
                "message": "Quiz me on this topic.",
                "action": "quiz_me",
            },
        )
        assert quiz_res.status_code == 200
        quiz_data = quiz_res.json()
        assert "Quiz" in quiz_data["reply"]


@pytest.mark.asyncio
async def test_ai_tutor_unauthorized():
    """Verify 401 Unauthorized for unauthenticated requests to AI Tutor."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/ai-tutor/chat",
            json={"message": "Hello tutor"},
        )
        assert res.status_code == 401
