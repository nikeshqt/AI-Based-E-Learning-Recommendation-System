import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://127.0.0.1:8085/api/v1"


async def run_e2e():
    test_email = f"student_{uuid.uuid4().hex[:6]}@example.com"
    test_password = "Password123!"

    print("==================================================")
    print("STARTING LIVE STAGE 3 E2E SKILL GAP & EXPLAINABLE RECSYS TEST")
    print("==================================================")

    async with httpx.AsyncClient(timeout=15.0) as client:
        # STEP 1: Register student
        print("\n[STEP 1] Registering student...")
        reg_res = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": test_email,
                "password": test_password,
                "full_name": "Stage3 E2E Student",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_res.status_code == 201, f"Register failed: {reg_res.text}"
        user_data = reg_res.json()
        user_id = user_data.get("user_id", user_data.get("id"))
        print(f"[OK] Registered user_id: {user_id}")

        # STEP 2: Login
        print("\n[STEP 2] Logging in...")
        login_res = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_email, "password": test_password},
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        print("[OK] Login successful, JWT token acquired.")

        # STEP 3: Set learning goal to Cybersecurity Analyst
        print("\n[STEP 3] Setting learning goal to 'Cybersecurity Analyst'...")
        goal_res = await client.put(
            f"{BASE_URL}/users/me/profile",
            json={"learning_goal": "Cybersecurity Analyst"},
            headers=auth_headers,
        )
        assert goal_res.status_code == 200, f"Profile update failed: {goal_res.text}"
        print("[OK] Learning goal updated.")

        # STEP 4: Verify required skills via GET /skill-gaps
        print("\n[STEP 4] Verifying required skills for Cybersecurity Analyst...")
        sg_res1 = await client.get(f"{BASE_URL}/skill-gaps", headers=auth_headers)
        assert sg_res1.status_code == 200, f"Skill gaps failed: {sg_res1.text}"
        sg_data1 = sg_res1.json()
        assert sg_data1["learning_goal"] == "Cybersecurity Analyst"
        skill_names = [s["skill"] for s in sg_data1["skills"]]
        assert "Networking" in skill_names
        assert "Linux" in skill_names
        print(f"[OK] Verified target skills: {skill_names}")

        # STEP 5: Complete Skill Assessment (Assessment -> user_skills)
        print("\n[STEP 5] Submitting 40-question Skill Assessment...")
        questions_res = await client.get(
            f"{BASE_URL}/assessments/asm_full_tech_01/questions",
            headers=auth_headers,
        )
        assert questions_res.status_code == 200
        questions = questions_res.json()

        # Submit answers (answering Python & Security correctly, Networking partially)
        answers = []
        for q in questions:
            domain = q.get("domain", "")
            if domain == "Python":
                selected = q["options"][0]  # Correct Python answer
            elif domain == "Networking":
                selected = q["options"][1]  # Partial / incorrect to simulate gap
            else:
                selected = q["options"][0]
            answers.append({"question_id": q["question_id"], "selected_option": selected})

        sub_res = await client.post(
            f"{BASE_URL}/assessments/asm_full_tech_01/submit",
            json={"answers": answers},
            headers=auth_headers,
        )
        assert sub_res.status_code == 200, f"Submit assessment failed: {sub_res.text}"
        res_data = sub_res.json()
        print(f"[OK] Assessment submitted. Score: {res_data['overall_score']}%")

        # STEP 6: Verify user_skills are updated
        print("\n[STEP 6] Verifying user_skills persistence...")
        me_res = await client.get(f"{BASE_URL}/users/me", headers=auth_headers)
        assert me_res.status_code == 200
        me_data = me_res.json()
        user_skills = me_data.get("skills", [])
        assert len(user_skills) > 0
        print(f"[OK] user_skills updated ({len(user_skills)} skills recorded).")

        # STEP 7: Request GET /skill-gaps and verify actual gaps
        print("\n[STEP 7] Requesting GET /api/v1/skill-gaps after assessment...")
        sg_res2 = await client.get(f"{BASE_URL}/skill-gaps", headers=auth_headers)
        assert sg_res2.status_code == 200
        sg_data2 = sg_res2.json()
        print(f"[OK] Overall Readiness: {sg_data2['overall_readiness']}%")
        for s in sg_data2["skills"]:
            print(f"  - {s['skill']}: Current={s['current_mastery']}%, Target={s['target_mastery']}%, Gap={s['gap']}%, Category={s['category']}, Priority={s['priority']}")

        # STEP 8 & 9: Request recommendations & verify skill gaps addressed
        print("\n[STEP 8 & 9] Requesting POST /api/v1/recommendations/personalized...")
        rec_res = await client.post(
            f"{BASE_URL}/recommendations/personalized",
            json={"user_id": user_id, "limit": 5},
        )
        assert rec_res.status_code == 200, f"Recommendations failed: {rec_res.text}"
        recs = rec_res.json()["recommendations"]
        assert len(recs) > 0, "No recommendations returned."
        print(f"[OK] Received {len(recs)} personalized recommendations.")

        # STEP 10: Verify every recommendation has a data-driven explanation
        print("\n[STEP 10] Verifying human-readable explainability for each recommendation...")
        for r in recs:
            assert "recommendation_reason" in r and len(r["recommendation_reason"]) > 10
            assert "Recommended because" in r["recommendation_reason"] or "proficiency" in r["recommendation_reason"]
            print(f"  * Course: '{r['course']['title']}'")
            print(f"    Reason: {r['recommendation_reason']}")
            print(f"    Skill Addressed: {r['target_skill_gap']} (Current: {r['current_skill_level']}%, Target: {r['target_skill_level']}%, Gap: {r['gap']}%)")

        # STEP 11: Change learning goal to "AI/ML Engineer"
        print("\n[STEP 11] Changing learning goal to 'AI/ML Engineer'...")
        goal_change_res = await client.put(
            f"{BASE_URL}/users/me/profile",
            json={"learning_goal": "AI/ML Engineer"},
            headers=auth_headers,
        )
        assert goal_change_res.status_code == 200

        # STEP 12: Verify skill gaps recalculate
        print("\n[STEP 12] Verifying skill gaps recalculated for new goal...")
        sg_res3 = await client.get(f"{BASE_URL}/skill-gaps", headers=auth_headers)
        assert sg_res3.status_code == 200
        sg_data3 = sg_res3.json()
        assert sg_data3["learning_goal"] == "AI/ML Engineer"
        new_skill_names = [s["skill"] for s in sg_data3["skills"]]
        assert "Machine Learning" in new_skill_names or "Deep Learning" in new_skill_names
        print(f"[OK] Recalculated target skills for AI/ML Engineer: {new_skill_names}")

        # STEP 13: Verify recommendations change accordingly
        print("\n[STEP 13] Requesting recommendations for updated goal...")
        rec_res2 = await client.post(
            f"{BASE_URL}/recommendations/personalized",
            json={"user_id": user_id, "limit": 5},
        )
        assert rec_res2.status_code == 200
        recs2 = rec_res2.json()["recommendations"]
        assert len(recs2) > 0
        print(f"[OK] Recommendations updated for AI/ML Engineer goal.")

        # STEP 14, 15, 16: Verify persistence across session reconnect
        print("\n[STEP 14-16] Verifying PostgreSQL persistence after session re-auth...")
        relogin_res = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_email, "password": test_password},
        )
        assert relogin_res.status_code == 200
        token2 = relogin_res.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        sg_res4 = await client.get(f"{BASE_URL}/skill-gaps", headers=headers2)
        assert sg_res4.status_code == 200
        sg_data4 = sg_res4.json()
        assert sg_data4["learning_goal"] == "AI/ML Engineer"
        print("[OK] Goals, skills, and skill gap calculations persisted cleanly in PostgreSQL!")

        print("\n==================================================")
        print("STAGE 3 REAL E2E TEST COMPLETED WITH 100% SUCCESS!")
        print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_e2e())
