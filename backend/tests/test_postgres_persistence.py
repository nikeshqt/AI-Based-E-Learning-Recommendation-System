import pytest
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal, init_db, Base
from app.models.user import UserModel, ProfileModel
from app.models.course import CourseCategoryModel, CourseModel, CourseSkillModel
from app.models.skill import SkillModel, UserSkillModel
from app.models.recommendation import RecommendationModel


@pytest.mark.asyncio
async def test_postgres_table_creation():
    """Verify all 15 required PostgreSQL tables are defined in metadata."""
    tables = Base.metadata.tables.keys()
    expected_tables = [
        "users",
        "profiles",
        "skills",
        "user_skills",
        "course_categories",
        "courses",
        "course_skills",
        "enrollments",
        "progress",
        "assessments",
        "quiz_results",
        "recommendations",
        "learning_paths",
        "learning_path_items",
        "analytics_events",
    ]
    for table_name in expected_tables:
        assert table_name in tables, f"Table {table_name} missing from metadata"


@pytest.mark.asyncio
async def test_postgres_user_profile_crud():
    """Verify CRUD operations and persistence for UserModel and ProfileModel."""
    await init_db()

    user_id = f"usr_test_{uuid.uuid4().hex[:6]}"
    email = f"test_{uuid.uuid4().hex[:6]}@ai-learning.io"

    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = UserModel(
                user_id=user_id,
                email=email,
                full_name="Persistence Tester",
                hashed_password="hashed_pw_test",
            )
            profile = ProfileModel(
                profile_id=f"prof_{uuid.uuid4().hex[:6]}",
                user_id=user_id,
                learning_goal="Cybersecurity Analyst",
                preferred_learning_style="visual",
                skill_level="intermediate",
            )
            session.add(user)
            session.add(profile)
            await session.commit()

    # Query back in new session
    async with AsyncSessionLocal() as session:
        stmt = select(UserModel).options(selectinload(UserModel.profile)).where(UserModel.user_id == user_id)
        result = await session.execute(stmt)
        queried_user = result.scalar_one_or_none()

        assert queried_user is not None
        assert queried_user.email == email
        assert queried_user.profile is not None
        assert queried_user.profile.learning_goal == "Cybersecurity Analyst"


@pytest.mark.asyncio
async def test_postgres_course_skills_crud():
    """Verify Course, Category, and Skill join relationship persistence."""
    await init_db()

    cat_id = f"cat_{uuid.uuid4().hex[:6]}"
    course_id = f"crs_{uuid.uuid4().hex[:6]}"
    skill_id = f"sk_{uuid.uuid4().hex[:6]}"

    async with AsyncSessionLocal() as session:
        async with session.begin():
            cat = CourseCategoryModel(category_id=cat_id, category_name=f"Category_{cat_id}", description="Test Category")
            skill = SkillModel(skill_id=skill_id, skill_name=f"Skill_{skill_id}", category="Security")
            course = CourseModel(
                course_id=course_id,
                title="Cybersecurity Operations",
                description="Threat analysis",
                instructor_name="Instructor",
                category_id=cat_id,
                category="Cybersecurity",
                difficulty_level="Intermediate",
                duration_hours=6.0,
            )
            course_skill = CourseSkillModel(
                id=f"cs_{uuid.uuid4().hex[:6]}",
                course_id=course_id,
                skill_id=skill_id,
                is_prerequisite=False,
            )
            session.add_all([cat, skill, course, course_skill])
            await session.commit()

    async with AsyncSessionLocal() as session:
        stmt = select(CourseModel).options(selectinload(CourseModel.course_skills)).where(CourseModel.course_id == course_id)
        res = await session.execute(stmt)
        queried_course = res.scalar_one_or_none()

        assert queried_course is not None
        assert queried_course.title == "Cybersecurity Operations"
        assert len(queried_course.course_skills) == 1
