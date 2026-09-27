import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_student_profile_and_data_isolation():
    """Verify Student A and Student B data isolation and profile boundaries in PostgreSQL."""
    email_a = f"studenta_{uuid.uuid4().hex[:6]}@test.com"
    email_b = f"studentb_{uuid.uuid4().hex[:6]}@test.com"
    password = "TestPassword123!"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Register Student A
        reg_a = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": email_a,
                "password": password,
                "full_name": "Student A",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_a.status_code in [200, 201]

        # 2. Register Student B
        reg_b = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": email_b,
                "password": password,
                "full_name": "Student B",
                "learning_goal": "Data Scientist",
            },
        )
        assert reg_b.status_code in [200, 201]

        # 3. Login Student A & verify profile
        login_a = await ac.post("/api/v1/auth/login", json={"email": email_a, "password": password})
        assert login_a.status_code == 200
        token_a = login_a.json()["access_token"]

        me_a = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_a}"})
        assert me_a.status_code == 200
        data_a = me_a.json()
        assert data_a["full_name"] == "Student A"
        assert data_a["email"].lower() == email_a.lower()
        assert data_a["learning_goal"] == "Cybersecurity Analyst"

        # 4. Login Student B & verify complete data isolation
        login_b = await ac.post("/api/v1/auth/login", json={"email": email_b, "password": password})
        assert login_b.status_code == 200
        token_b = login_b.json()["access_token"]

        me_b = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_b}"})
        assert me_b.status_code == 200
        data_b = me_b.json()
        assert data_b["full_name"] == "Student B"
        assert data_b["email"].lower() == email_b.lower()
        assert data_b["learning_goal"] == "Data Scientist"

        # Student B MUST NOT see Student A details
        assert data_b["full_name"] != data_a["full_name"]
        assert data_b["email"] != data_a["email"]

        # 5. Login Student A again & verify persistence
        me_a_again = await ac.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_a}"})
        assert me_a_again.status_code == 200
        assert me_a_again.json()["email"].lower() == email_a.lower()
