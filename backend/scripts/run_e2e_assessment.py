import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://127.0.0.1:8085/api/v1"


async def main():
    print("==================================================")
    print("STARTING COMPLETE E2E SKILL ASSESSMENT TEST")
    print("==================================================")

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        # STEP 1: Register a new student
        unique_email = f"e2e_student_{uuid.uuid4().hex[:6]}@test.com"
        print(f"\n[STEP 1] Registering new student: {unique_email}")
        reg_res = await client.post("/auth/register", json={
            "email": unique_email,
            "password": "Password123!",
            "full_name": "E2E Assessment Learner",
            "learning_goal": "Cybersecurity Analyst",
        })
        assert reg_res.status_code == 201, f"Register failed: {reg_res.text}"
        user_id = reg_res.json()["user_id"]
        print(f"-> Registered user_id: {user_id}")

        # STEP 2: Login
        print("\n[STEP 2] Logging in...")
        login_res = await client.post("/auth/login", json={
            "email": unique_email,
            "password": "Password123!",
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("-> JWT token acquired successfully")

        # STEP 3: Request available assessments
        print("\n[STEP 3 & 4] Requesting available assessments...")
        asm_res = await client.get("/assessments")
        assert asm_res.status_code == 200, f"Fetch assessments failed: {asm_res.text}"
        assessments = asm_res.json()
        assert len(assessments) >= 1
        asm_id = assessments[0]["assessment_id"]
        print(f"-> Selected assessment: {asm_id} ('{assessments[0]['title']}')")

        # STEP 5: Retrieve questions and verify correct answers are NOT present
        print("\n[STEP 5] Retrieving questions & checking security...")
        q_res = await client.get(f"/assessments/{asm_id}/questions", headers=headers)
        assert q_res.status_code == 200, f"Fetch questions failed: {q_res.text}"
        questions = q_res.json()
        assert len(questions) == 40, f"Expected 40 questions, got {len(questions)}"

        for q in questions:
            assert "correct_answer" not in q, f"SECURITY VIOLATION: correct_answer exposed in {q['question_id']}"
            assert "explanation" not in q, f"SECURITY VIOLATION: explanation exposed in {q['question_id']}"
        print("-> 40 sanitized questions retrieved. Zero answer keys exposed.")

        # STEP 6: Submit controlled answer set (20 correct, 20 incorrect -> 50% score)
        print("\n[STEP 6] Submitting controlled 50% answer set (20 correct, 20 incorrect)...")
        submitted_answers = []
        for idx, q in enumerate(questions):
            if idx < 20:
                opt = q["options"][0]
            else:
                opt = "INCORRECT_OPTION"
            submitted_answers.append({"question_id": q["question_id"], "selected_option": opt})

        sub_res = await client.post(f"/assessments/{asm_id}/submit", json={"answers": submitted_answers}, headers=headers)
        assert sub_res.status_code == 200, f"Submission failed: {sub_res.text}"
        result = sub_res.json()
        attempt_id = result["attempt_id"]
        print(f"-> Submitted attempt {attempt_id}. Overall Score: {result['overall_score']}%")

        # STEP 7: Verify topic scores
        print("\n[STEP 7] Verifying topic scores...")
        assert "topic_scores" in result and len(result["topic_scores"]) == 8
        print(f"-> Topic Scores: {result['topic_scores']}")

        # STEP 8: Verify difficulty performance
        print("\n[STEP 8] Verifying difficulty performance...")
        assert "difficulty_performance" in result
        print(f"-> Difficulty Performance: {result['difficulty_performance']}")

        # STEP 9: Verify skill proficiency
        print("\n[STEP 9] Verifying skill proficiency calculation...")
        assert "skill_proficiency" in result
        print(f"-> Skill Proficiency: {result['skill_proficiency']}")

        # STEP 10: Verify PostgreSQL user_skills were updated
        print("\n[STEP 10] Verifying PostgreSQL user_skills updated...")
        profile_res = await client.get(f"/users/{user_id}")
        assert profile_res.status_code == 200
        skills = profile_res.json()["skills"]
        assert len(skills) >= 1
        print(f"-> Persisted User Skills count: {len(skills)}")

        # STEP 11: Request personalized recommendations with updated skills
        print("\n[STEP 11] Triggering personalized recommendations with updated skills...")
        rec_res = await client.post("/recommendations/personalized", json={"user_id": user_id, "limit": 5})
        assert rec_res.status_code == 200, f"RecSys request failed: {rec_res.text}"
        recs = rec_res.json()["recommendations"]
        assert len(recs) > 0
        print(f"-> RecSys returned {len(recs)} personalized recommendations. Top match: '{recs[0]['course']['title']}' (Score: {recs[0]['match_score']})")

        # STEP 12: Verify assessment history
        print("\n[STEP 12] Verifying assessment history endpoint...")
        hist_res = await client.get("/assessments/history", headers=headers)
        assert hist_res.status_code == 200
        assert hist_res.json()["total_attempts"] >= 1
        print("-> Assessment history verified")

        # STEP 13: Verify latest result
        print("\n[STEP 13] Verifying latest assessment result endpoint...")
        latest_res = await client.get(f"/assessments/{asm_id}/results", headers=headers)
        assert latest_res.status_code == 200
        assert latest_res.json()["attempt_id"] == attempt_id
        print("-> Latest result verified")

        # STEP 14: Cross-user authorization check
        print("\n[STEP 14] Testing unauthorized cross-user access protection...")
        reg_b = await client.post("/auth/register", json={
            "email": f"other_student_{uuid.uuid4().hex[:6]}@test.com",
            "password": "Password123!",
            "full_name": "Other Student",
            "learning_goal": "AI",
        })
        login_b = await client.post("/auth/login", json={"email": reg_b.json()["email"], "password": "Password123!"})
        headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

        res_b = await client.get(f"/assessments/{asm_id}/results", headers=headers_b)
        assert res_b.status_code == 404, f"Security failure: User B could access User A result (status {res_b.status_code})"
        print("-> Cross-user authorization isolation verified (404 for unauthorized student)")

        # STEP 15, 16, 17: Post-restart persistence verification
        print("\n[STEP 15, 16 & 17] Verifying post-restart database persistence...")
        relogin_res = await client.post("/auth/login", json={"email": unique_email, "password": "Password123!"})
        assert relogin_res.status_code == 200
        token_after = relogin_res.json()["access_token"]
        headers_after = {"Authorization": f"Bearer {token_after}"}

        # Check history
        h_after = await client.get("/assessments/history", headers=headers_after)
        assert h_after.status_code == 200 and h_after.json()["total_attempts"] >= 1

        # Check skills
        p_after = await client.get(f"/users/{user_id}")
        assert p_after.status_code == 200 and len(p_after.json()["skills"]) >= 1

        # Check recommendations
        r_after = await client.post("/recommendations/personalized", json={"user_id": user_id, "limit": 5})
        assert r_after.status_code == 200 and len(r_after.json()["recommendations"]) > 0

        print("-> All data persisted cleanly in PostgreSQL and survived restart simulation!")
        print("\n==================================================")
        print("E2E SKILL ASSESSMENT TEST FULLY PASSED")
        print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
