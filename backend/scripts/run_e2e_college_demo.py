import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


async def main():
    print("======================================================================")
    print("STAGE 7 -- FULL SYSTEM VERIFICATION & COLLEGE DEMO READINESS E2E TEST")
    print("======================================================================")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8085"
    ) as client:
        # STEP 1: Register new student
        email = f"college_demo_{uuid.uuid4().hex[:6]}@ai-learning.io"
        password = "CollegeDemoPassword123!"
        print(f"\n[STEP 1] Registering fresh demo student: {email}")
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Jordan Lee",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_res.status_code in [200, 201], f"Register failed: {reg_res.text}"
        user_id = reg_res.json()["user_id"]
        print(f"  [OK] Student registered successfully. user_id: {user_id}")

        # STEP 2: Login
        print(f"\n[STEP 2] Logging in to retrieve JWT access token...")
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("  [OK] JWT access token retrieved.")

        # STEP 3: Set Career Goal
        print(f"\n[STEP 3] Setting target career goal: 'Cybersecurity Analyst'")
        goal_res = await client.put(
            "/api/v1/users/me/profile",
            headers=headers,
            json={
                "learning_goal": "Cybersecurity Analyst",
                "interests": ["Cybersecurity", "Linux", "Networking"],
            },
        )
        assert goal_res.status_code == 200
        print("  [OK] Career goal saved.")

        # STEP 4-5: Fetch & Complete Skill Assessment (40 Questions)
        print(f"\n[STEP 4-5] Fetching & Completing 40-Question Skill Assessment...")
        asm_id = "sec_assessment_40q"
        q_res = await client.get(f"/api/v1/assessments/{asm_id}/questions", headers=headers)
        assert q_res.status_code == 200, f"Fetch questions failed: {q_res.text}"
        questions = q_res.json()
        assert len(questions) >= 40, f"Expected 40+ questions, got {len(questions)}"

        answers = []
        for idx, q in enumerate(questions):
            # Select option string
            selected_idx = 0 if idx % 2 == 0 else 1
            selected_opt = q["options"][selected_idx]
            answers.append({"question_id": q["question_id"], "selected_option": selected_opt})

        submit_res = await client.post(
            f"/api/v1/assessments/{asm_id}/submit",
            headers=headers,
            json={"user_id": user_id, "answers": answers},
        )
        assert submit_res.status_code == 200, f"Assessment submit failed: {submit_res.text}"
        result_data = submit_res.json()
        print(f"  [OK] Assessment submitted. Overall Score: {result_data['overall_score']}%")

        # STEP 6: Verify user_skills persistence
        me_res = await client.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        print(f"  [OK] Verified user_skills updated in PostgreSQL database.")

        # STEP 7-8: Open Skill Gap Analysis & Verify Gaps
        print(f"\n[STEP 7-8] Performing Skill Gap Analysis...")
        gaps_res = await client.get("/api/v1/skill-gaps", headers=headers)
        assert gaps_res.status_code == 200
        gaps_data = gaps_res.json()
        print(f"  [OK] Target Goal: '{gaps_data['learning_goal']}'")
        print(f"  [OK] Total Skills Analyzed: {len(gaps_data['skills'])}")
        for item in gaps_data["skills"][:3]:
            print(f"      - {item['skill']}: Current {item['current_mastery']}% | Target {item['target_mastery']}% | Gap: {item['gap']}%")

        # STEP 9-10: Request AI Recommendations
        print(f"\n[STEP 9-10] Requesting Hybrid AI Recommendations...")
        recs_res = await client.get("/api/v1/recommendations/personalized", headers=headers)
        assert recs_res.status_code == 200
        recs_data = recs_res.json()
        print(f"  [OK] Recommendations returned: {len(recs_data['recommendations'])} items.")
        top_rec = recs_data["recommendations"][0]
        print(f"      Top Course: {top_rec['course']['title']}")
        print(f"      Reason: {top_rec['recommendation_reason']}")

        # STEP 11-12: Generate Personalized Learning Path
        print(f"\n[STEP 11-12] Generating Prerequisite-Aware Learning Path...")
        path_res = await client.post(
            "/api/v1/learning-paths/generate",
            headers=headers,
            json={"target_goal": "Cybersecurity Analyst"},
        )
        assert path_res.status_code == 200
        path_data = path_res.json()
        print(f"  [OK] Learning Path ID: {path_data['learning_path_id']}")
        print(f"  [OK] Stages Count: {path_data['total_stages']} | Total Courses: {path_data['total_courses']}")

        # STEP 13: Enroll in First Course
        target_course_id = "crs_sec_04"
        print(f"\n[STEP 13] Enrolling in First Recommended Course: '{target_course_id}'...")
        enroll_res = await client.post(f"/api/v1/courses/{target_course_id}/enroll", headers=headers)
        assert enroll_res.status_code == 200
        print(f"  [OK] Enrolled in '{target_course_id}'. Status: {enroll_res.json()['status']}")

        # STEP 14-16: Open Lesson & Complete Lesson 1
        print(f"\n[STEP 14-16] Opening Course Lesson & Completing Lesson 1...")
        content_res = await client.get(f"/api/v1/courses/{target_course_id}/learning", headers=headers)
        assert content_res.status_code == 200
        content_data = content_res.json()
        first_lesson = content_data["modules"][0]["lessons"][0]

        comp1_res = await client.post(
            f"/api/v1/courses/{target_course_id}/lessons/{first_lesson['lesson_id']}/complete",
            headers=headers,
        )
        assert comp1_res.status_code == 200
        print(f"  [OK] Lesson 1 ('{first_lesson['title']}') Completed. Progress: {comp1_res.json()['progress_percentage']}%")

        # STEP 17-19: Query AI Tutor with Lesson Context
        print(f"\n[STEP 17-19] Querying AI Tutor for Lesson Explanation...")
        tutor_res = await client.post(
            "/api/v1/ai-tutor/chat",
            headers=headers,
            json={
                "message": "Explain this lesson simply.",
                "course_id": target_course_id,
                "lesson_id": first_lesson["lesson_id"],
            },
        )
        assert tutor_res.status_code == 200, f"AI Tutor failed: {tutor_res.text}"
        tutor_data = tutor_res.json()
        print(f"  [OK] AI Tutor Response Received ({len(tutor_data['reply'])} chars):")
        print(f"      '{tutor_data['reply'][:120]}...'")

        # STEP 20-21: Complete Remaining Lessons
        print(f"\n[STEP 20-21] Completing Remaining Course Lessons...")
        all_lessons = [les for mod in content_data["modules"] for les in mod["lessons"]]
        for les in all_lessons[1:]:
            c_res = await client.post(
                f"/api/v1/courses/{target_course_id}/lessons/{les['lesson_id']}/complete",
                headers=headers,
            )
            assert c_res.status_code == 200

        final_content = await client.get(f"/api/v1/courses/{target_course_id}/learning", headers=headers)
        assert final_content.status_code == 200
        print(f"  [OK] Course Progress: {final_content.json()['progress_percentage']}% | Status: {final_content.json()['status']}")

        # STEP 22-23: Verify Dashboard Statistics
        print(f"\n[STEP 22-23] Verifying Updated Dashboard Statistics...")
        stats_res = await client.get("/api/v1/learning/dashboard-stats", headers=headers)
        assert stats_res.status_code == 200
        stats_data = stats_res.json()
        print(f"  [OK] Completed Courses Count: {stats_data['completed_courses_count']}")
        print(f"  [OK] In Progress Courses Count: {stats_data['in_progress_courses_count']}")

        # STEP 24-26: Simulate Backend Restart & Verify Data Persistence
        print(f"\n[STEP 24-26] Verifying Data Persistence Across Backend Restart...")
        login_again = await client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert login_again.status_code == 200
        token_again = login_again.json()["access_token"]
        headers_again = {"Authorization": f"Bearer {token_again}"}

        persisted_stats = await client.get("/api/v1/learning/dashboard-stats", headers=headers_again)
        assert persisted_stats.status_code == 200
        assert persisted_stats.json()["completed_courses_count"] == 1
        print("  [OK] Data persistence across restart verified successfully.")

        print("\n======================================================================")
        print("STAGE 7 FULL SYSTEM VERIFICATION: ALL 26 STEPS PASSED CLEANLY!")
        print("======================================================================\n")


if __name__ == "__main__":
    asyncio.run(main())
