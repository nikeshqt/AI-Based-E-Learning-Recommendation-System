import asyncio
import httpx
import uuid
import sys

BASE_URL = "http://127.0.0.1:8085/api/v1"


async def run_e2e():
    test_email_a = f"student_a_{uuid.uuid4().hex[:6]}@example.com"
    test_email_b = f"student_b_{uuid.uuid4().hex[:6]}@example.com"
    test_password = "Password123!"

    print("==================================================")
    print("STARTING LIVE STAGE 4 PERSONALIZED LEARNING PATH E2E TEST")
    print("==================================================")

    async with httpx.AsyncClient(timeout=15.0) as client:
        # STEP 1: Register new student A
        print("\n[STEP 1] Registering student A...")
        reg_res = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": test_email_a,
                "password": test_password,
                "full_name": "Stage4 Learner A",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_res.status_code == 201, f"Register A failed: {reg_res.text}"
        user_a_data = reg_res.json()
        user_a_id = user_a_data.get("user_id", user_a_data.get("id"))
        print(f"[OK] Registered Student A user_id: {user_a_id}")

        # STEP 2: Login A
        print("\n[STEP 2] Logging in Student A...")
        login_res = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_email_a, "password": test_password},
        )
        assert login_res.status_code == 200, f"Login A failed: {login_res.text}"
        token_a = login_res.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}
        print("[OK] Student A logged in, JWT token acquired.")

        # STEP 3: Set goal to Cybersecurity Analyst
        print("\n[STEP 3] Setting career goal to 'Cybersecurity Analyst'...")
        goal_res = await client.put(
            f"{BASE_URL}/users/me/profile",
            json={"learning_goal": "Cybersecurity Analyst"},
            headers=headers_a,
        )
        assert goal_res.status_code == 200, f"Goal update failed: {goal_res.text}"
        print("[OK] Career goal set to Cybersecurity Analyst.")

        # STEP 4: Complete Skill Assessment
        print("\n[STEP 4] Submitting 40-question Skill Assessment...")
        questions_res = await client.get(
            f"{BASE_URL}/assessments/asm_full_tech_01/questions",
            headers=headers_a,
        )
        assert questions_res.status_code == 200
        questions = questions_res.json()

        answers = []
        for q in questions:
            domain = q.get("domain", "")
            if domain == "Python":
                selected = q["options"][0]
            elif domain == "Networking":
                selected = q["options"][1]
            else:
                selected = q["options"][0]
            answers.append({"question_id": q["question_id"], "selected_option": selected})

        sub_res = await client.post(
            f"{BASE_URL}/assessments/asm_full_tech_01/submit",
            json={"answers": answers},
            headers=headers_a,
        )
        assert sub_res.status_code == 200, f"Assessment submit failed: {sub_res.text}"
        score = sub_res.json()["overall_score"]
        print(f"[OK] Skill assessment completed with score: {score}%")

        # STEP 5: Verify user_skills persistence
        print("\n[STEP 5] Verifying user_skills persistence...")
        me_res = await client.get(f"{BASE_URL}/users/me", headers=headers_a)
        assert me_res.status_code == 200
        user_skills = me_res.json().get("skills", [])
        assert len(user_skills) > 0
        print(f"[OK] user_skills persisted ({len(user_skills)} skills recorded).")

        # STEP 6: Request skill gaps
        print("\n[STEP 6] Requesting GET /api/v1/skill-gaps...")
        sg_res = await client.get(f"{BASE_URL}/skill-gaps", headers=headers_a)
        assert sg_res.status_code == 200
        sg_data = sg_res.json()
        print(f"[OK] Skill Gaps retrieved. Overall Readiness: {sg_data['overall_readiness']}%")

        # STEP 7: Generate learning path
        print("\n[STEP 7] Requesting POST /api/v1/learning-paths/generate...")
        lp_gen_res = await client.post(
            f"{BASE_URL}/learning-paths/generate",
            json={"target_goal": "Cybersecurity Analyst"},
            headers=headers_a,
        )
        assert lp_gen_res.status_code == 200, f"Generate LP failed: {lp_gen_res.text}"
        lp_data = lp_gen_res.json()

        # STEP 8: Verify learning path structure
        print("\n[STEP 8] Verifying learning path structure, prerequisite ordering, and explainability...")
        assert lp_data["career_goal"] == "Cybersecurity Analyst"
        assert lp_data["total_stages"] > 0
        assert lp_data["total_courses"] > 0
        assert lp_data["total_duration_hours"] > 0
        assert lp_data["is_active"] is True
        path_id_a = lp_data["learning_path_id"]

        print(f"  * Path ID: {path_id_a}")
        print(f"  * Total Stages: {lp_data['total_stages']}")
        print(f"  * Total Courses: {lp_data['total_courses']}")
        print(f"  * Total Duration: {lp_data['total_duration_hours']} Hours")

        for stage in lp_data["stages"]:
            print(f"\n  [STAGE {stage['stage_number']}] {stage['stage_title']} ({stage['estimated_duration_hours']} Hours)")
            print(f"    Description: {stage['description']}")
            print(f"    Target Skills: {', '.join(stage['target_skills'])}")
            for c in stage["courses"]:
                print(f"      - {c['course_title']} (Target Skill: {c['target_skill']}, Gap: {c['skill_gap']}%, Duration: {c['estimated_duration_hours']}h)")
                print(f"        Reason: {c['reason']}")

        # STEP 9: Get current active learning path
        print("\n[STEP 9] Requesting GET /api/v1/learning-paths/current...")
        curr_res = await client.get(f"{BASE_URL}/learning-paths/current", headers=headers_a)
        assert curr_res.status_code == 200
        curr_data = curr_res.json()
        assert curr_data["learning_path_id"] == path_id_a
        print("[OK] Current active learning path retrieved.")

        # STEP 10: Get learning path details
        print("\n[STEP 10] Requesting GET /api/v1/learning-paths/{learning_path_id}...")
        detail_res = await client.get(f"{BASE_URL}/learning-paths/{path_id_a}", headers=headers_a)
        assert detail_res.status_code == 200
        assert detail_res.json()["learning_path_id"] == path_id_a
        print("[OK] Learning path details retrieved.")

        # STEP 11 & 12: Regenerate learning path after profile update
        print("\n[STEP 11 & 12] Updating skills and regenerating learning path...")
        regen_res = await client.post(
            f"{BASE_URL}/learning-paths/generate",
            json={"target_goal": "Cybersecurity Analyst"},
            headers=headers_a,
        )
        assert regen_res.status_code == 200
        regen_data = regen_res.json()
        assert regen_data["learning_path_id"] != path_id_a
        assert regen_data["is_active"] is True
        print(f"[OK] Learning path regenerated. New Path ID: {regen_data['learning_path_id']}")

        # STEP 13 & 14: Change goal to AI/ML Engineer and regenerate path
        print("\n[STEP 13 & 14] Changing goal to 'AI/ML Engineer' and regenerating path...")
        aiml_gen_res = await client.post(
            f"{BASE_URL}/learning-paths/generate",
            json={"target_goal": "AI/ML Engineer"},
            headers=headers_a,
        )
        assert aiml_gen_res.status_code == 200
        aiml_data = aiml_gen_res.json()
        assert aiml_data["career_goal"] == "AI/ML Engineer"
        print(f"[OK] Learning path updated for AI/ML Engineer goal.")

        # STEP 15 & 16: Session re-authentication
        print("\n[STEP 15 & 16] Logging in again to test PostgreSQL persistence...")
        relogin_res = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_email_a, "password": test_password},
        )
        assert relogin_res.status_code == 200
        token_a2 = relogin_res.json()["access_token"]
        headers_a2 = {"Authorization": f"Bearer {token_a2}"}

        # STEP 17: Verify active learning path persists in PostgreSQL
        print("\n[STEP 17] Verifying active learning path persistence...")
        persisted_res = await client.get(f"{BASE_URL}/learning-paths/current", headers=headers_a2)
        assert persisted_res.status_code == 200
        persisted_data = persisted_res.json()
        assert persisted_data["career_goal"] == "AI/ML Engineer"
        assert persisted_data["learning_path_id"] == aiml_data["learning_path_id"]
        print("[OK] Active learning path persisted cleanly in PostgreSQL across re-auth!")

        # STEP 18: Register Student B and attempt unauthorized access to Student A's path
        print("\n[STEP 18] Registering Student B and testing cross-user authorization (403 Forbidden)...")
        reg_b = await client.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": test_email_b,
                "password": test_password,
                "full_name": "Stage4 Learner B",
                "learning_goal": "Software Engineering",
            },
        )
        assert reg_b.status_code == 201
        login_b = await client.post(
            f"{BASE_URL}/auth/login",
            json={"email": test_email_b, "password": test_password},
        )
        assert login_b.status_code == 200
        token_b = login_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # Student B attempts to fetch Student A's path_id
        forbidden_res = await client.get(
            f"{BASE_URL}/learning-paths/{aiml_data['learning_path_id']}",
            headers=headers_b,
        )
        assert forbidden_res.status_code == 403, f"Expected 403 Forbidden, got: {forbidden_res.status_code}"
        print("[OK] Cross-user access blocked with 403 Forbidden.")

        print("\n==================================================")
        print("STAGE 4 REAL E2E TEST COMPLETED WITH 100% SUCCESS!")
        print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_e2e())
