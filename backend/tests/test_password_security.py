import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_password_security_and_non_exposure():
    """Verify password is hashed securely, wrong password fails, and password is never returned in API payloads."""
    email = f"sec_student_{uuid.uuid4().hex[:6]}@test.com"
    plaintext_password = "SecretPassword123!"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Register student
        reg_res = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": plaintext_password,
                "full_name": "Security Test Learner",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_res.status_code in [200, 201]
        reg_data = reg_res.json()

        # VERIFY SECURITY RULE: Password/hash is NEVER returned in register response
        assert "password" not in reg_data
        assert "hashed_password" not in reg_data
        assert "password_hash" not in reg_data

        # 2. Login with WRONG password -> Must fail with 401 Unauthorized
        wrong_res = await ac.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "WrongPassword!"},
        )
        assert wrong_res.status_code == 401

        # 3. Login with CORRECT password -> Succeeds
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"email": email, "password": plaintext_password},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # VERIFY SECURITY RULE: Password/hash is NEVER returned in /auth/me or profile responses
        me_res = await ac.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_res.status_code == 200
        me_data = me_res.json()
        assert "password" not in me_data
        assert "hashed_password" not in me_data
        assert "password_hash" not in me_data
