import sys
import uuid
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db

async def run_isolation_verification():
    print("==================================================")
    print("STARTING MULTI-STUDENT DATA ISOLATION VERIFICATION")
    print("==================================================")
    
    # Initialize DB models
    await init_db()
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Register & Login Student A
        uid_a = str(uuid.uuid4())[:8]
        email_a = f"student_a_{uid_a}@test.com"
        pass_a = "Password123!"
        
        reg_a = await client.post("/api/v1/auth/register", json={
            "full_name": f"Student A ({uid_a})",
            "email": email_a,
            "learning_goal": "Cybersecurity Analyst",
            "password": pass_a,
        })
        assert reg_a.status_code in (200, 201), f"Registration A failed: {reg_a.text}"
        user_a_data = reg_a.json()
        user_a_id = user_a_data["user_id"]

        login_a = await client.post("/api/v1/auth/login", json={
            "email": email_a,
            "password": pass_a
        })
        assert login_a.status_code == 200, f"Login A failed: {login_a.text}"
        token_a = login_a.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}
        print(f"[SUCCESS] Student A registered & logged in: user_id={user_a_id}")

        # Step 2: Register & Login Student B
        uid_b = str(uuid.uuid4())[:8]
        email_b = f"student_b_{uid_b}@test.com"
        pass_b = "Password123!"
        
        reg_b = await client.post("/api/v1/auth/register", json={
            "full_name": f"Student B ({uid_b})",
            "email": email_b,
            "learning_goal": "AI Engineer",
            "password": pass_b,
        })
        assert reg_b.status_code in (200, 201), f"Registration B failed: {reg_b.text}"
        user_b_data = reg_b.json()
        user_b_id = user_b_data["user_id"]

        login_b = await client.post("/api/v1/auth/login", json={
            "email": email_b,
            "password": pass_b
        })
        assert login_b.status_code == 200, f"Login B failed: {login_b.text}"
        token_b = login_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}
        print(f"[SUCCESS] Student B registered & logged in: user_id={user_b_id}")

        # Step 3: Verify Password Privacy
        for user_obj in [user_a_data, user_b_data]:
            assert "password" not in user_obj, "Security risk: password found in user response!"
            assert "password_hash" not in user_obj, "Security risk: password_hash found in user response!"
            assert "hashed_password" not in user_obj, "Security risk: hashed_password found in user response!"
        print("[SUCCESS] Password non-exposure verified for both students.")

        # Step 4: Verify Initial Empty State for Student B
        me_b = await client.get("/api/v1/users/me", headers=headers_b)
        assert me_b.status_code == 200
        assert me_b.json()["email"] == email_b
        assert me_b.json()["user_id"] == user_b_id
        assert me_b.json()["user_id"] != user_a_id

        # Step 5: Student A completes assessment
        asm_list_res = await client.get("/api/v1/assessments", headers=headers_a)
        assert asm_list_res.status_code == 200
        asm_list = asm_list_res.json()
        assert len(asm_list) > 0, "No assessments found!"
        target_asm = asm_list[0]
        asm_id = target_asm["assessment_id"]

        questions_res = await client.get(f"/api/v1/assessments/{asm_id}/questions", headers=headers_a)
        assert questions_res.status_code == 200, f"Failed fetching questions for {asm_id}: {questions_res.text}"
        q_list = questions_res.json()

        answers = [{"question_id": q["question_id"], "selected_option": q["options"][0]} for q in q_list]
        sub_a = await client.post(f"/api/v1/assessments/{asm_id}/submit", headers=headers_a, json={
            "answers": answers,
            "time_taken_seconds": 120
        })
        assert sub_a.status_code == 200, f"Assessment submission A failed: {sub_a.text}"
        print(f"[SUCCESS] Student A completed assessment {asm_id} with score {sub_a.json()['overall_score']}%")

        # Step 6: Student A generates learning path
        path_a_res = await client.post("/api/v1/learning-paths/generate", headers=headers_a, json={
            "target_goal": "Cybersecurity Analyst"
        })
        assert path_a_res.status_code == 200, f"Learning path generation A failed: {path_a_res.text}"
        path_a_id = path_a_res.json()["learning_path_id"]
        print(f"[SUCCESS] Student A created Learning Path: {path_a_id}")

        # Step 7: Verify Student B CANNOT see Student A's data
        # 7a: Skill gaps for B
        gaps_b = await client.get("/api/v1/skill-gaps", headers=headers_b)
        assert gaps_b.status_code == 200
        assert gaps_b.json()["user_id"] == user_b_id
        assert gaps_b.json()["learning_goal"] == "AI Engineer"
        print("[SUCCESS] Student B /skill-gaps belongs strictly to Student B.")

        # 7b: Recommendations for B
        recs_b = await client.get("/api/v1/recommendations/personalized", headers=headers_b)
        assert recs_b.status_code == 200
        assert recs_b.json()["user_id"] == user_b_id
        print("[SUCCESS] Student B /recommendations belongs strictly to Student B.")

        # 7c: Student B attempts to directly access Student A's learning path by path_id -> Must be 403 Forbidden
        path_cross_access = await client.get(f"/api/v1/learning-paths/{path_a_id}", headers=headers_b)
        assert path_cross_access.status_code == 403, (
            f"Cross-student privacy breach! Expected 403 Forbidden, got {path_cross_access.status_code}"
        )
        print(f"[SUCCESS] Cross-student access control verified: Student B denied access to Student A's path ({path_a_id}).")

        # Step 8: Verify Student A still retrieves their own learning path
        path_own_access = await client.get(f"/api/v1/learning-paths/{path_a_id}", headers=headers_a)
        assert path_own_access.status_code == 200
        assert path_own_access.json()["learning_path_id"] == path_a_id
        print("[SUCCESS] Student A can retrieve their own learning path.")

    print("==================================================")
    print("ALL MULTI-STUDENT DATA ISOLATION VERIFICATIONS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_isolation_verification())
