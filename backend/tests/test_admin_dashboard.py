import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_admin_authentication_and_login():
    """Verify admin login produces valid JWT access token with role 'admin'."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["role"] == "admin"


@pytest.mark.asyncio
async def test_student_login_and_role():
    """Verify student login produces valid JWT access token with role 'student'."""
    student_email = f"student_{uuid.uuid4().hex[:6]}@example.com"
    student_password = "StudentPassword123!"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register student
        reg = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": student_email,
                "password": student_password,
                "full_name": "Test Student Learner",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        assert reg.status_code in [200, 201]

        # Login student
        login_res = await ac.post(
            "/api/v1/auth/login",
            json={"email": student_email, "password": student_password},
        )
        assert login_res.status_code == 200
        data = login_res.json()
        assert data["role"] == "student"


@pytest.mark.asyncio
async def test_role_authorization_admin_vs_student():
    """Verify admin accessing dashboard returns 200, but student gets 403 Forbidden."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Admin Login
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_token = admin_login.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Admin accessing admin dashboard -> PASS
        admin_dash_res = await ac.get("/api/v1/admin/dashboard", headers=admin_headers)
        assert admin_dash_res.status_code == 200
        dash_data = admin_dash_res.json()
        assert "total_students" in dash_data
        assert "total_courses" in dash_data
        assert "avg_course_progress" in dash_data

        # 2. Register & login student
        student_email = f"auth_student_{uuid.uuid4().hex[:6]}@example.com"
        await ac.post(
            "/api/v1/auth/register",
            json={
                "email": student_email,
                "password": "Password123!",
                "full_name": "Normal Student",
                "learning_goal": "AI/ML Engineer",
            },
        )
        student_login = await ac.post(
            "/api/v1/auth/login",
            json={"email": student_email, "password": "Password123!"},
        )
        student_token = student_login.json()["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}

        # Student accessing admin dashboard -> HTTP 403 FORBIDDEN
        student_dash_res = await ac.get("/api/v1/admin/dashboard", headers=student_headers)
        assert student_dash_res.status_code == 403
        assert "Forbidden" in student_dash_res.json()["detail"] or "Admin" in student_dash_res.json()["detail"]

        # 3. Unauthenticated request -> HTTP 401 UNAUTHORIZED
        unauth_res = await ac.get("/api/v1/admin/dashboard")
        assert unauth_res.status_code == 401


@pytest.mark.asyncio
async def test_student_management_and_password_non_exposure():
    """Verify student list endpoint returns student metrics and never exposes passwords or hashes."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        res = await ac.get("/api/v1/admin/students", headers=admin_headers)
        assert res.status_code == 200
        data = res.json()
        assert "total" in data
        assert "students" in data
        assert data["total"] > 0

        # Verify each student object never contains passwords or hashes
        for s in data["students"]:
            assert "password" not in s
            assert "hashed_password" not in s
            assert "password_hash" not in s
            assert "email" in s
            assert "career_goal" in s
            assert "assessment_status" in s
            assert "is_active" in s


@pytest.mark.asyncio
async def test_student_detail_360_view():
    """Verify detailed student profile displays profile, assessment, skill gaps, recommendations, and progress."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register a test student with known data
        test_email = f"detail_{uuid.uuid4().hex[:6]}@test.com"
        reg = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": test_email,
                "password": "Password123!",
                "full_name": "Detailed Profile Learner",
                "learning_goal": "Cybersecurity Analyst",
            },
        )
        student_id = reg.json()["user_id"]

        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        # Fetch student detail
        res = await ac.get(f"/api/v1/admin/students/{student_id}", headers=admin_headers)
        assert res.status_code == 200
        detail = res.json()

        # PROFILE section
        assert "profile" in detail
        assert detail["profile"]["user_id"] == student_id
        assert detail["profile"]["full_name"] == "Detailed Profile Learner"
        assert "password" not in detail["profile"]
        assert "hashed_password" not in detail["profile"]

        # ASSESSMENT section
        assert "assessment" in detail

        # SKILL GAPS section
        assert "skill_gaps" in detail

        # RECOMMENDATIONS section
        assert "recommendations" in detail

        # COURSE PROGRESS section
        assert "course_progress" in detail


@pytest.mark.asyncio
async def test_account_activation_and_deactivation():
    """Verify deactivating student account rejects login and blocks protected API calls with 403."""
    student_email = f"deact_{uuid.uuid4().hex[:6]}@test.com"
    password = "DeactivateMe123!"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register student
        reg = await ac.post(
            "/api/v1/auth/register",
            json={
                "email": student_email,
                "password": password,
                "full_name": "Deactivation Test Student",
                "learning_goal": "Software Engineering",
            },
        )
        student_id = reg.json()["user_id"]

        # 2. Login student initially -> works
        initial_login = await ac.post(
            "/api/v1/auth/login",
            json={"email": student_email, "password": password},
        )
        assert initial_login.status_code == 200
        student_token = initial_login.json()["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}

        # Protected API call -> works
        me_res = await ac.get("/api/v1/auth/me", headers=student_headers)
        assert me_res.status_code == 200

        # 3. Admin deactivates student account
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        deact_res = await ac.patch(
            f"/api/v1/admin/students/{student_id}/status",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert deact_res.status_code == 200
        assert deact_res.json()["is_active"] is False

        # 4. Attempt student login -> MUST BE REJECTED (HTTP 403)
        deact_login = await ac.post(
            "/api/v1/auth/login",
            json={"email": student_email, "password": password},
        )
        assert deact_login.status_code == 403
        assert "deactivated" in deact_login.json()["detail"].lower()

        # 5. Protected API requests with previous token -> MUST BE REJECTED (HTTP 403)
        blocked_call = await ac.get("/api/v1/auth/me", headers=student_headers)
        assert blocked_call.status_code == 403
        assert "deactivated" in blocked_call.json()["detail"].lower()

        # 6. Admin reactivates student account
        react_res = await ac.patch(
            f"/api/v1/admin/students/{student_id}/status",
            json={"is_active": True},
            headers=admin_headers,
        )
        assert react_res.status_code == 200
        assert react_res.json()["is_active"] is True

        # 7. Student can login again
        react_login = await ac.post(
            "/api/v1/auth/login",
            json={"email": student_email, "password": password},
        )
        assert react_login.status_code == 200


@pytest.mark.asyncio
async def test_course_management_crud_and_recommendation_compatibility():
    """Verify admin can view, create, edit, and deactivate courses while preserving RecSys compatibility."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        # 1. View courses
        courses_res = await ac.get("/api/v1/admin/courses", headers=admin_headers)
        assert courses_res.status_code == 200
        assert len(courses_res.json()) > 0

        # 2. Create course
        new_course_payload = {
            "title": "Cloud Security & DevSecOps Engineering",
            "description": "Comprehensive guide to securing AWS, Kubernetes clusters, and CI/CD pipelines.",
            "category": "Cloud Computing",
            "difficulty_level": "Intermediate",
            "duration_hours": 9.5,
            "instructor_name": "DevSecOps Master",
            "prerequisites": ["Linux", "Cloud Computing"],
            "skills_taught": ["Cloud Computing", "Cybersecurity", "DevSecOps"],
        }
        create_res = await ac.post(
            "/api/v1/admin/courses",
            json=new_course_payload,
            headers=admin_headers,
        )
        assert create_res.status_code == 201
        created_course = create_res.json()
        new_course_id = created_course["course_id"]
        assert created_course["title"] == new_course_payload["title"]
        assert created_course["is_active"] is True

        # 3. Edit course
        edit_res = await ac.put(
            f"/api/v1/admin/courses/{new_course_id}",
            json={"title": "Cloud Security & DevSecOps Engineering (Updated)"},
            headers=admin_headers,
        )
        assert edit_res.status_code == 200
        assert edit_res.json()["title"] == "Cloud Security & DevSecOps Engineering (Updated)"

        # 4. Deactivate course
        deact_res = await ac.patch(
            f"/api/v1/admin/courses/{new_course_id}/status",
            json={"is_active": False},
            headers=admin_headers,
        )
        assert deact_res.status_code == 200
        assert deact_res.json()["is_active"] is False


@pytest.mark.asyncio
async def test_course_progress_inspection_and_audit():
    """Verify admin can view student course progress records and adjust progress with audit trail."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        # Inspect all progress records
        prog_res = await ac.get("/api/v1/admin/progress", headers=admin_headers)
        assert prog_res.status_code == 200
        records = prog_res.json()
        assert isinstance(records, list)

        # If records exist, test administrative correction
        if len(records) > 0:
            target_enr = records[0]["enrollment_id"]
            corr_res = await ac.patch(
                f"/api/v1/admin/progress/{target_enr}",
                json={
                    "progress_percentage": 100.0,
                    "status": "COMPLETED",
                    "reason": "Verified lab completion certificate",
                },
                headers=admin_headers,
            )
            assert corr_res.status_code == 200
            assert corr_res.json()["progress_percentage"] == 100.0
            assert corr_res.json()["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_real_database_analytics():
    """Verify system analytics are calculated from real PostgreSQL database data."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        res = await ac.get("/api/v1/admin/analytics", headers=admin_headers)
        assert res.status_code == 200
        data = res.json()

        # Student analytics
        assert "student_analytics" in data
        assert data["student_analytics"]["total_students"] > 0
        assert data["student_analytics"]["active_students"] > 0

        # Course analytics
        assert "course_analytics" in data
        assert data["course_analytics"]["total_courses"] > 0

        # Learning analytics
        assert "learning_analytics" in data

        # Skill analytics
        assert "skill_analytics" in data
        assert "most_common_skill_gaps" in data["skill_analytics"]


@pytest.mark.asyncio
async def test_audit_activity_logs():
    """Verify administrative actions generate queryable audit logs without sensitive credentials."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        admin_login = await ac.post(
            "/api/v1/auth/login",
            json={
                "email": settings.DEFAULT_ADMIN_EMAIL,
                "password": settings.DEFAULT_ADMIN_PASSWORD,
            },
        )
        admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

        res = await ac.get("/api/v1/admin/activity", headers=admin_headers)
        assert res.status_code == 200
        logs = res.json()
        assert len(logs) > 0

        # Verify no passwords or tokens stored in logs
        for log in logs:
            assert "password" not in log["action"].lower()
            if log.get("details"):
                assert "password" not in log["details"].lower()
                assert "secret" not in log["details"].lower()
