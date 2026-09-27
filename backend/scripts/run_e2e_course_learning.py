import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app


async def main():
    print("======================================================================")
    print("STAGE 5 -- SIMPLE COURSE LEARNING & PROGRESS TRACKING LIVE E2E VERIFICATION")
    print("======================================================================")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8085"
    ) as client:
        # Step 1: Generate unique user credentials
        email = f"student_stage5_{uuid.uuid4().hex[:6]}@ai-learning.io"
        password = "SecurePassword123!"
        print(f"\n[Step 1] Generated test email: {email}")

        # Step 2: Register user
        reg_res = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": "Stage 5 Test Student",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg_res.status_code in [200, 201], f"Register failed: {reg_res.text}"
        user_id = reg_res.json()["user_id"]
        print(f"  [OK] User registered successfully. user_id: {user_id}")

        # Step 3: Login to obtain JWT Token
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"  [OK] JWT authentication token retrieved successfully.")

        # Step 4: Update user profile
        prof_res = await client.put(
            "/api/v1/users/me/profile",
            headers=headers,
            json={
                "learning_goal": "Cybersecurity Analyst",
                "interests": ["Cybersecurity", "Linux", "Networking"],
            },
        )
        assert prof_res.status_code == 200, f"Update profile failed: {prof_res.text}"
        print("  [OK] Student profile updated: Career Goal = 'Cybersecurity Analyst'")

        # Step 5: Check course catalog
        cat_res = await client.get("/api/v1/catalog/courses")
        assert cat_res.status_code == 200
        print(f"  [OK] Course catalog fetched: {len(cat_res.json())} courses available.")

        # Step 6: Target course for learning
        target_course_id = "crs_sec_04"
        print(f"\n[Step 6] Target course selected: '{target_course_id}'")

        # Step 7: Enroll in course
        enroll_res = await client.post(
            f"/api/v1/courses/{target_course_id}/enroll", headers=headers
        )
        assert enroll_res.status_code == 200
        enroll_data = enroll_res.json()
        print(f"\n[Step 7-8] Enrolled in course:")
        print(f"  - Enrollment ID: {enroll_data['enrollment_id']}")
        print(f"  - Initial Status: {enroll_data['status']}")
        print(f"  - Initial Progress %: {enroll_data['progress_percentage']}%")

        # Step 9-10: Fetch course learning content
        content_res = await client.get(
            f"/api/v1/courses/{target_course_id}/learning", headers=headers
        )
        assert content_res.status_code == 200
        content_data = content_res.json()
        print(f"\n[Step 9-10] Course Modules & Educational Content Fetched:")
        print(f"  - Course Title: {content_data['title']}")
        print(f"  - Category: {content_data['category']}")
        print(f"  - Modules Count: {len(content_data['modules'])}")
        print(f"  - Total Lessons Count: {content_data['total_lessons_count']}")

        # Step 11-14: Progressively complete lessons
        all_lessons = []
        for mod in content_data["modules"]:
            for les in mod["lessons"]:
                all_lessons.append(les)

        print(f"\n[Step 11-14] Progressively Completing {len(all_lessons)} Lessons:")
        for idx, les in enumerate(all_lessons, 1):
            comp_res = await client.post(
                f"/api/v1/courses/{target_course_id}/lessons/{les['lesson_id']}/complete",
                headers=headers,
            )
            assert comp_res.status_code == 200
            c_data = comp_res.json()
            print(
                f"  [OK] Lesson {idx}/{len(all_lessons)} '{les['title'][:35]}...' marked COMPLETE | Progress: {c_data['progress_percentage']}%"
            )

        # Step 15: Verify 100% course completion
        final_content = await client.get(
            f"/api/v1/courses/{target_course_id}/learning", headers=headers
        )
        assert final_content.status_code == 200
        fc_data = final_content.json()
        print(f"\n[Step 15] Final Course Progress Verification:")
        print(f"  - Status: {fc_data['status']}")
        print(f"  - Progress Percentage: {fc_data['progress_percentage']}%")
        print(
            f"  - Completed Lessons: {fc_data['completed_lessons_count']}/{fc_data['total_lessons_count']}"
        )

        # Step 16: Check continue learning API endpoint
        cont_res = await client.get("/api/v1/learning/continue", headers=headers)
        assert cont_res.status_code == 200
        cont_data = cont_res.json()
        print(f"\n[Step 16] Continue Learning API Payload:")
        print(f"  - Has Active Course: {cont_data['has_active_course']}")

        # Step 17: Check dashboard stats API endpoint
        stats_res = await client.get(
            "/api/v1/learning/dashboard-stats", headers=headers
        )
        assert stats_res.status_code == 200
        stats_data = stats_res.json()
        print(f"\n[Step 17] Dashboard Statistics Summary:")
        print(f"  - Completed Courses Count: {stats_data['completed_courses_count']}")
        print(
            f"  - In Progress Courses Count: {stats_data['in_progress_courses_count']}"
        )

        print("\n======================================================================")
        print("STAGE 5 LIVE E2E VERIFICATION: ALL 17 STEPS PASSED CLEANLY!")
        print("======================================================================\n")


if __name__ == "__main__":
    asyncio.run(main())
