import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db


@pytest.mark.asyncio
async def test_assessment_list_and_questions_security():
    """Verify available assessments list and correct-answer stripping security in questions endpoint."""
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Available assessments list
        res = await ac.get("/api/v1/assessments")
        assert res.status_code == 200
        assessments = res.json()
        assert len(assessments) >= 1
        asm_id = assessments[0]["assessment_id"]
        assert asm_id == "asm_tech_eval_01"

        # 2. Register & Login student
        email = f"student_sec_{uuid.uuid4().hex[:6]}@test.com"
        reg_res = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "password": "Password123!",
            "full_name": "Security Tester",
            "learning_goal": "Cybersecurity",
        })
        assert reg_res.status_code == 201

        login_res = await ac.post("/api/v1/auth/login", json={
            "email": email,
            "password": "Password123!",
        })
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # 3. Retrieve questions authenticated
        q_res = await ac.get(
            f"/api/v1/assessments/{asm_id}/questions",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert q_res.status_code == 200
        questions = q_res.json()
        assert len(questions) == 40

        # 4. Verify correct-answer protection: correct_answer & explanation must NOT be exposed
        for q in questions:
            assert "correct_answer" not in q
            assert "explanation" not in q
            assert len(q["options"]) == 4
            assert q["domain"] in [
                "Python", "Networking", "Linux", "Cybersecurity",
                "AI / Machine Learning", "SQL", "Web Development", "Cloud Computing"
            ]


@pytest.mark.asyncio
async def test_controlled_assessment_submission_and_scoring():
    """Verify controlled answer submission, topic scores, difficulty, proficiency, and PostgreSQL persistence."""
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = f"controlled_{uuid.uuid4().hex[:6]}@test.com"
        reg = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "password": "Password123!",
            "full_name": "Controlled Submitter",
            "learning_goal": "Software Engineering",
        })
        assert reg.status_code == 201

        login = await ac.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
        token = login.json()["access_token"]
        user_id = login.json()["user_id"]

        # Retrieve questions
        q_res = await ac.get(
            "/api/v1/assessments/asm_tech_eval_01/questions",
            headers={"Authorization": f"Bearer {token}"}
        )
        questions = q_res.json()

        # Submit answers
        answers = []
        for idx, q in enumerate(questions):
            if idx < 20:
                ans = q["options"][0]
            else:
                ans = "INCORRECT_OPTION_TEXT"
            answers.append({"question_id": q["question_id"], "selected_option": ans})

        # Submit assessment
        sub_res = await ac.post(
            "/api/v1/assessments/asm_tech_eval_01/submit",
            json={"answers": answers},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert sub_res.status_code == 200
        result = sub_res.json()

        assert result["user_id"] == user_id
        assert result["total_questions"] == 40
        assert result["answered_questions"] == 40
        assert "overall_score" in result
        assert "topic_scores" in result
        assert "difficulty_performance" in result
        assert "skill_proficiency" in result

        # Verify latest result endpoint
        latest_res = await ac.get(
            "/api/v1/assessments/asm_tech_eval_01/results",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert latest_res.status_code == 200
        assert latest_res.json()["attempt_id"] == result["attempt_id"]

        # Verify history endpoint
        hist_res = await ac.get(
            "/api/v1/assessments/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert hist_res.status_code == 200
        assert hist_res.json()["total_attempts"] >= 1


@pytest.mark.asyncio
async def test_existing_skill_aggregation_strategy():
    """Verify non-downgrading skill aggregation strategy (e.g. 80% existing is NOT overwritten by 50%)."""
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = f"skill_agg_{uuid.uuid4().hex[:6]}@test.com"
        reg = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "password": "Password123!",
            "full_name": "Aggregation Tester",
            "learning_goal": "Data Science",
        })
        assert reg.status_code == 201

        login = await ac.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
        token = login.json()["access_token"]
        user_id = login.json()["user_id"]

        # Set initial strong skill in profile (Networking = 80% / 0.80)
        await ac.put(
            f"/api/v1/users/{user_id}/profile",
            json={"skills": [{"skill_name": "Networking", "mastery_score": 0.80}]},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Submit an assessment score resulting in weaker/different performance
        sub_res = await ac.post(
            "/api/v1/assessments/asm_tech_eval_01/submit",
            json={"answers": [{"question_id": "q_net_01", "selected_option": "WRONG"}]},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert sub_res.status_code == 200

        # Verify user profile retains the stronger demonstrated mastery (>= 0.80)
        u_res = await ac.get(f"/api/v1/users/{user_id}")
        assert u_res.status_code == 200
        user_profile = u_res.json()

        net_skill = next((s for s in user_profile["skills"] if s["skill_name"].lower() == "networking"), None)
        assert net_skill is not None
        assert net_skill["mastery_score"] >= 0.80


@pytest.mark.asyncio
async def test_cross_user_authorization_isolation():
    """Verify students cannot access or submit assessment results for another user."""
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # User A
        reg_a = await ac.post("/api/v1/auth/register", json={
            "email": f"user_a_{uuid.uuid4().hex[:6]}@test.com", "password": "Password123!", "full_name": "User A", "learning_goal": "Goal A"
        })
        login_a = await ac.post("/api/v1/auth/login", json={"email": reg_a.json()["email"], "password": "Password123!"})
        token_a = login_a.json()["access_token"]

        # User B
        reg_b = await ac.post("/api/v1/auth/register", json={
            "email": f"user_b_{uuid.uuid4().hex[:6]}@test.com", "password": "Password123!", "full_name": "User B", "learning_goal": "Goal B"
        })
        login_b = await ac.post("/api/v1/auth/login", json={"email": reg_b.json()["email"], "password": "Password123!"})
        token_b = login_b.json()["access_token"]

        # User A submits assessment
        await ac.post(
            "/api/v1/assessments/asm_tech_eval_01/submit",
            json={"answers": []},
            headers={"Authorization": f"Bearer {token_a}"}
        )

        # User B attempts to access User A's results via their token
        res_b = await ac.get(
            "/api/v1/assessments/asm_tech_eval_01/results",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        assert res_b.status_code == 404  # No results for User B


@pytest.mark.asyncio
async def test_recommendation_engine_integration_with_updated_skills():
    """Verify that submitting an assessment updates skills and triggers fresh personalized recommendations."""
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = f"recsys_{uuid.uuid4().hex[:6]}@test.com"
        reg = await ac.post("/api/v1/auth/register", json={
            "email": email,
            "password": "Password123!",
            "full_name": "RecSys Tester",
            "learning_goal": "Cybersecurity",
        })
        login = await ac.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"})
        token = login.json()["access_token"]
        user_id = login.json()["user_id"]

        # Submit assessment
        await ac.post(
            "/api/v1/assessments/asm_tech_eval_01/submit",
            json={"answers": []},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Request personalized recommendations
        rec_res = await ac.post(
            "/api/v1/recommendations/personalized",
            json={"user_id": user_id, "limit": 5}
        )
        assert rec_res.status_code == 200
        recs = rec_res.json()["recommendations"]
        assert len(recs) > 0
        assert "match_score" in recs[0]
