import uuid
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc, or_
from app.core.database import AsyncSessionLocal
from app.models.user import UserModel, ProfileModel
from app.models.course import CourseModel, CourseCategoryModel, CourseModuleModel, CourseLessonModel, CourseSkillModel
from app.models.learning import EnrollmentModel, ProgressModel
from app.models.assessment import AssessmentAttemptModel, AssessmentQuestionModel
from app.models.recommendation import LearningPathModel, LearningPathItemModel
from app.models.skill import SkillModel, UserSkillModel, GoalRequiredSkillModel
from app.models.admin_log import AdminActivityLogModel
from app.schemas.admin import (
    AdminDashboardStats,
    AdminStudentListItem,
    AdminStudentListResponse,
    AdminStudentDetailResponse,
    StudentProfileSection,
    StudentAssessmentSection,
    StudentSkillGapSection,
    StudentRecommendationSection,
    StudentLearningPathSection,
    StudentLearningPathStage,
    StudentCourseProgressSection,
    AdminCourseItem,
    AdminCourseCreate,
    AdminCourseUpdate,
    AdminProgressItem,
    AdminProgressUpdate,
    AdminAnalyticsResponse,
    StudentAnalyticsData,
    CourseAnalyticsData,
    LearningAnalyticsData,
    SkillAnalyticsData,
    AdminActivityItem,
)
from app.schemas.course import CourseResponse, LessonSchema
from app.services.skill_gap_service import skill_gap_service
from app.services.recsys_service import recsys_service
from app.services.learning_path_service import learning_path_service
from app.services.catalog_service import catalog_service


class AdminService:
    """Service providing administrative queries, data operations, analytics, and audit logging."""

    async def record_activity(
        self,
        admin_id: Optional[str],
        action: str,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        details: Optional[str] = None,
    ) -> AdminActivityItem:
        """Create an audit log record for an administrative action."""
        log_id = f"log_{uuid.uuid4().hex[:10]}"
        now_utc = datetime.now(timezone.utc)
        async with AsyncSessionLocal() as session:
            try:
                log_entry = AdminActivityLogModel(
                    log_id=log_id,
                    admin_id=admin_id,
                    action=action,
                    target_type=target_type,
                    target_id=target_id,
                    details=details,
                    created_at=now_utc,
                )
                session.add(log_entry)
                await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[AdminService] Warning logging activity: {err}")

        return AdminActivityItem(
            log_id=log_id,
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
            timestamp=now_utc,
        )

    async def get_dashboard_stats(self) -> AdminDashboardStats:
        """Calculate high-level dashboard metrics across PostgreSQL entities."""
        async with AsyncSessionLocal() as session:
            # 1. Total students & Active students
            stmt_students = select(UserModel).where(UserModel.role != "admin")
            res_students = await session.execute(stmt_students)
            students = res_students.scalars().all()
            total_students = len(students)
            active_students = sum(1 for s in students if getattr(s, "is_active", True))

            # 2. Total Courses
            stmt_courses = select(func.count(CourseModel.course_id))
            res_courses = await session.execute(stmt_courses)
            total_courses = res_courses.scalar() or 0

            # 3. Total Enrollments & Completions & Avg Progress
            stmt_enrollments = select(EnrollmentModel)
            res_enrollments = await session.execute(stmt_enrollments)
            enrollments = res_enrollments.scalars().all()
            total_enrollments = len(enrollments)
            courses_completed = sum(
                1 for e in enrollments if (e.status == "COMPLETED" or (e.progress_percentage or 0.0) >= 100.0)
            )
            if total_enrollments > 0:
                avg_course_progress = round(
                    sum(e.progress_percentage or 0.0 for e in enrollments) / total_enrollments, 1
                )
            else:
                avg_course_progress = 0.0

            # 4. Assessment Completion Rate
            stmt_assessed_users = select(func.count(func.distinct(AssessmentAttemptModel.user_id)))
            res_assessed = await session.execute(stmt_assessed_users)
            assessed_count = res_assessed.scalar() or 0
            if total_students > 0:
                assessment_completion_rate = round((assessed_count / total_students) * 100.0, 1)
            else:
                assessment_completion_rate = 0.0

            # 5. Recent Activity Logs
            stmt_logs = (
                select(AdminActivityLogModel, UserModel)
                .outerjoin(UserModel, AdminActivityLogModel.admin_id == UserModel.user_id)
                .order_by(desc(AdminActivityLogModel.created_at))
                .limit(8)
            )
            res_logs = await session.execute(stmt_logs)
            log_rows = res_logs.all()
            recent_activity: List[AdminActivityItem] = []
            for log_model, user_model in log_rows:
                recent_activity.append(
                    AdminActivityItem(
                        log_id=log_model.log_id,
                        admin_id=log_model.admin_id,
                        admin_name=user_model.full_name if user_model else "Administrator",
                        admin_email=user_model.email if user_model else None,
                        action=log_model.action,
                        target_type=log_model.target_type,
                        target_id=log_model.target_id,
                        details=log_model.details,
                        timestamp=log_model.created_at,
                    )
                )

            # 6. Career goal distribution
            stmt_goals = (
                select(ProfileModel.learning_goal, func.count(ProfileModel.profile_id))
                .group_by(ProfileModel.learning_goal)
            )
            res_goals = await session.execute(stmt_goals)
            goal_distribution = [
                {"name": row[0] or "General AI", "value": row[1]} for row in res_goals.all()
            ]

            # 7. Enrollment trend (by month/date)
            stmt_trend = (
                select(func.date(EnrollmentModel.enrolled_at), func.count(EnrollmentModel.enrollment_id))
                .group_by(func.date(EnrollmentModel.enrolled_at))
                .order_by(func.date(EnrollmentModel.enrolled_at))
                .limit(7)
            )
            res_trend = await session.execute(stmt_trend)
            enrollment_trends = [
                {"date": str(row[0] or "Recent"), "enrollments": row[1]} for row in res_trend.all()
            ]
            if not enrollment_trends and total_enrollments > 0:
                enrollment_trends = [{"date": "Active Session", "enrollments": total_enrollments}]

            return AdminDashboardStats(
                total_students=total_students,
                active_students=active_students,
                total_courses=total_courses,
                total_enrollments=total_enrollments,
                courses_completed=courses_completed,
                avg_course_progress=avg_course_progress,
                assessment_completion_rate=assessment_completion_rate,
                recent_activity=recent_activity,
                enrollment_trends=enrollment_trends,
                goal_distribution=goal_distribution,
            )

    async def list_students(
        self,
        search: Optional[str] = None,
        career_goal: Optional[str] = None,
        assessment_status: Optional[str] = None,
        account_status: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> AdminStudentListResponse:
        """List students with search, filters, sorting, and aggregated metrics."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(UserModel)
                .options(
                    selectinload(UserModel.profile),
                    selectinload(UserModel.enrollments),
                    selectinload(UserModel.assessment_attempts),
                )
                .where(UserModel.role != "admin")
            )

            if search:
                term = f"%{search.strip().lower()}%"
                stmt = stmt.where(
                    or_(
                        func.lower(UserModel.full_name).like(term),
                        func.lower(UserModel.email).like(term),
                    )
                )

            res = await session.execute(stmt)
            users = res.scalars().all()

            student_items: List[AdminStudentListItem] = []
            for u in users:
                prof = u.profile
                c_goal = prof.learning_goal if prof else "General AI"
                s_level = prof.skill_level if prof else "beginner"

                # Filter by career goal if specified
                if career_goal and career_goal.lower() not in c_goal.lower():
                    continue

                # Account status filter
                is_act = getattr(u, "is_active", True)
                if account_status == "active" and not is_act:
                    continue
                if account_status == "inactive" and is_act:
                    continue

                # Assessment status & score
                attempts = u.assessment_attempts or []
                has_assessed = len(attempts) > 0
                latest_score = attempts[-1].overall_score if has_assessed else None
                ass_status = "Completed" if has_assessed else "Not Completed"

                if assessment_status:
                    if assessment_status.lower() == "completed" and not has_assessed:
                        continue
                    if assessment_status.lower() in ["not_completed", "not completed", "pending"] and has_assessed:
                        continue

                # Enrolled courses count & overall progress
                enrs = u.enrollments or []
                enr_count = len(enrs)
                if enr_count > 0:
                    prog_avg = round(sum(e.progress_percentage or 0.0 for e in enrs) / enr_count, 1)
                else:
                    prog_avg = 0.0

                student_items.append(
                    AdminStudentListItem(
                        user_id=u.user_id,
                        full_name=u.full_name,
                        email=u.email,
                        career_goal=c_goal,
                        skill_level=s_level,
                        role=getattr(u, "role", "student"),
                        is_active=is_act,
                        created_at=u.created_at,
                        last_login=getattr(u, "last_login", None),
                        assessment_status=ass_status,
                        assessment_score=latest_score,
                        enrolled_courses_count=enr_count,
                        overall_progress=prog_avg,
                    )
                )

            # Sort results
            reverse = (sort_order.lower() == "desc")
            if sort_by == "name":
                student_items.sort(key=lambda x: x.full_name.lower(), reverse=reverse)
            elif sort_by == "email":
                student_items.sort(key=lambda x: x.email.lower(), reverse=reverse)
            elif sort_by == "progress":
                student_items.sort(key=lambda x: x.overall_progress, reverse=reverse)
            else:
                student_items.sort(
                    key=lambda x: x.created_at or datetime.fromtimestamp(0, tz=timezone.utc),
                    reverse=reverse,
                )

            return AdminStudentListResponse(total=len(student_items), students=student_items)

    async def get_student_detail(self, student_id: str) -> Optional[AdminStudentDetailResponse]:
        """Fetch full 360-degree profile for selected student across all LMS modules."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(UserModel)
                .options(
                    selectinload(UserModel.profile),
                    selectinload(UserModel.assessment_attempts),
                    selectinload(UserModel.enrollments).selectinload(EnrollmentModel.course),
                    selectinload(UserModel.skills).selectinload(UserSkillModel.skill),
                )
                .where(UserModel.user_id == student_id)
            )
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()

            if not user:
                return None

            prof = user.profile
            profile_sec = StudentProfileSection(
                user_id=user.user_id,
                full_name=user.full_name,
                email=user.email,
                career_goal=prof.learning_goal if prof else "General AI",
                preferred_learning_style=prof.preferred_learning_style if prof else "visual",
                skill_level=prof.skill_level if prof else "beginner",
                is_active=getattr(user, "is_active", True),
                role=getattr(user, "role", "student"),
                registration_date=user.created_at,
                last_login=getattr(user, "last_login", None),
            )

            # Assessment Details
            attempts = user.assessment_attempts or []
            if attempts:
                latest_attempt = attempts[-1]
                ass_sec = StudentAssessmentSection(
                    completed=True,
                    overall_score=latest_attempt.overall_score,
                    topic_scores=latest_attempt.topic_scores or {},
                    difficulty_performance=latest_attempt.difficulty_performance or {},
                    skill_proficiency=latest_attempt.skill_proficiency or {},
                    total_questions=latest_attempt.total_questions,
                    correct_answers=latest_attempt.correct_answers,
                    submitted_at=latest_attempt.submitted_at,
                )
            else:
                ass_sec = StudentAssessmentSection(completed=False)

            # Skill Gaps
            gaps_list: List[StudentSkillGapSection] = []
            try:
                skill_gap_res = await skill_gap_service.calculate_user_skill_gaps(student_id)
                for item in skill_gap_res.skills:
                    gaps_list.append(
                        StudentSkillGapSection(
                            skill=item.skill,
                            current_mastery=item.current_mastery,
                            target_mastery=item.target_mastery,
                            gap=item.gap,
                            priority=item.priority,
                            category=item.category,
                        )
                    )
            except Exception as e:
                print(f"[AdminService] Warning calculating gaps for {student_id}: {e}")

            # Recommendations
            recs_list: List[StudentRecommendationSection] = []
            try:
                recs_resp = await recsys_service.get_personalized_recommendations(student_id, limit=4)
                for r in recs_resp.recommendations:
                    recs_list.append(
                        StudentRecommendationSection(
                            course_id=r.course.course_id,
                            title=r.course.title,
                            match_score=r.match_score,
                            recommendation_reason=r.recommendation_reason,
                            target_skill_gap=r.target_skill_gap,
                        )
                    )
            except Exception as e:
                print(f"[AdminService] Warning fetching recs for {student_id}: {e}")

            # Learning Path
            lp_sec = None
            try:
                path_resp = await learning_path_service.get_active_path_for_user(student_id)
                if path_resp:
                    stages = []
                    for st in path_resp.stages:
                        stages.append(
                            StudentLearningPathStage(
                                stage_number=st.stage_number,
                                stage_title=st.stage_title,
                                course_id=st.course_id,
                                course_title=st.course_title,
                                status=st.status,
                                target_skill=st.target_skill,
                            )
                        )
                    lp_sec = StudentLearningPathSection(
                        path_id=path_resp.learning_path_id,
                        title=path_resp.title,
                        overall_readiness=path_resp.overall_readiness,
                        is_active=path_resp.is_active,
                        stages=stages,
                    )
            except Exception as e:
                print(f"[AdminService] Warning fetching path for {student_id}: {e}")

            # Course Progress
            progress_sec: List[StudentCourseProgressSection] = []
            for enr in user.enrollments or []:
                course = enr.course
                # Query completed lessons from progress table
                stmt_prog = select(func.count(ProgressModel.progress_id)).where(
                    ProgressModel.user_id == student_id,
                    ProgressModel.course_id == enr.course_id,
                    ProgressModel.is_completed == True,
                )
                res_prog = await session.execute(stmt_prog)
                completed_count = res_prog.scalar() or 0

                # Query total lessons
                stmt_lessons = select(func.count(CourseLessonModel.lesson_id)).where(
                    CourseLessonModel.course_id == enr.course_id
                )
                res_lessons = await session.execute(stmt_lessons)
                total_count = res_lessons.scalar() or 0
                if total_count == 0:
                    total_count = 4  # Default fallback lesson count

                # Last activity
                stmt_last = select(func.max(ProgressModel.last_watched_at)).where(
                    ProgressModel.user_id == student_id,
                    ProgressModel.course_id == enr.course_id,
                )
                res_last = await session.execute(stmt_last)
                last_act = res_last.scalar() or enr.enrolled_at

                progress_sec.append(
                    StudentCourseProgressSection(
                        course_id=enr.course_id,
                        course_title=course.title if course else enr.course_id,
                        category=course.category if course else "General",
                        enrollment_date=enr.enrolled_at,
                        progress_percentage=enr.progress_percentage or 0.0,
                        completed_lessons=completed_count,
                        total_lessons=total_count,
                        completion_status=enr.status or "ENROLLED",
                        last_activity=last_act,
                    )
                )

            return AdminStudentDetailResponse(
                profile=profile_sec,
                assessment=ass_sec,
                skill_gaps=gaps_list,
                recommendations=recs_list,
                learning_path=lp_sec,
                course_progress=progress_sec,
            )

    async def update_student_status(
        self, student_id: str, is_active: bool, admin_id: str
    ) -> bool:
        """Activate or deactivate student account with audit logging."""
        async with AsyncSessionLocal() as session:
            stmt = select(UserModel).where(UserModel.user_id == student_id)
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()
            if not user:
                return False

            user.is_active = is_active
            await session.commit()

        action = "STUDENT_ACTIVATED" if is_active else "STUDENT_DEACTIVATED"
        status_text = "activated" if is_active else "deactivated"
        await self.record_activity(
            admin_id=admin_id,
            action=action,
            target_type="student",
            target_id=student_id,
            details=f"Student account {user.email} was {status_text} by administrator",
        )
        return True

    async def list_courses(self) -> List[AdminCourseItem]:
        """List all catalog courses with enrolled student counts and module/lesson totals."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(CourseModel)
                .options(
                    selectinload(CourseModel.modules).selectinload(CourseModuleModel.lessons),
                    selectinload(CourseModel.course_skills).selectinload(CourseSkillModel.skill),
                    selectinload(CourseModel.enrollments),
                )
                .order_by(desc(CourseModel.created_at))
            )
            res = await session.execute(stmt)
            courses = res.scalars().all()

            results: List[AdminCourseItem] = []
            for c in courses:
                prereqs: List[str] = []
                taught: List[str] = []
                for cs in c.course_skills:
                    s_name = cs.skill.skill_name if cs.skill else cs.skill_id
                    if cs.is_prerequisite:
                        prereqs.append(s_name)
                    else:
                        taught.append(s_name)

                mod_count = len(c.modules)
                les_count = sum(len(m.lessons) for m in c.modules)

                results.append(
                    AdminCourseItem(
                        course_id=c.course_id,
                        title=c.title,
                        description=c.description,
                        instructor_name=c.instructor_name,
                        category=c.category,
                        difficulty_level=c.difficulty_level,
                        duration_hours=c.duration_hours,
                        rating=c.rating or 5.0,
                        enrolled_count=len(c.enrollments) or (c.enrolled_count or 0),
                        is_active=getattr(c, "is_active", True),
                        prerequisites=prereqs,
                        skills_taught=taught,
                        modules_count=mod_count,
                        lessons_count=les_count,
                        created_at=c.created_at,
                    )
                )

            # Fallback if DB courses list is empty
            if not results:
                for c in catalog_service._courses:
                    results.append(
                        AdminCourseItem(
                            course_id=c.course_id,
                            title=c.title,
                            description=c.description,
                            instructor_name=c.instructor_name,
                            category=c.category,
                            difficulty_level=c.difficulty_level,
                            duration_hours=c.duration_hours,
                            rating=c.rating,
                            enrolled_count=c.enrolled_count,
                            is_active=True,
                            prerequisites=c.prerequisites,
                            skills_taught=c.skills_taught,
                            modules_count=1,
                            lessons_count=len(c.lessons),
                            created_at=datetime.now(timezone.utc),
                        )
                    )

            return results

    async def create_course(
        self, course_in: AdminCourseCreate, admin_id: str
    ) -> AdminCourseItem:
        """Create new course compatible with AI RecSys engine and persistent catalog."""
        new_id = f"crs_{uuid.uuid4().hex[:6]}"
        now_utc = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as session:
            try:
                # 1. Ensure category exists
                stmt_cat = select(CourseCategoryModel).where(
                    CourseCategoryModel.category_name == course_in.category
                )
                res_cat = await session.execute(stmt_cat)
                cat_obj = res_cat.scalar_one_or_none()
                if not cat_obj:
                    cat_obj = CourseCategoryModel(
                        category_id=f"cat_{uuid.uuid4().hex[:6]}",
                        category_name=course_in.category,
                        description=f"{course_in.category} Catalog",
                    )
                    session.add(cat_obj)
                    await session.flush()

                # 2. Create course
                new_course = CourseModel(
                    course_id=new_id,
                    title=course_in.title,
                    description=course_in.description,
                    instructor_name=course_in.instructor_name,
                    category_id=cat_obj.category_id,
                    category=course_in.category,
                    difficulty_level=course_in.difficulty_level,
                    duration_hours=course_in.duration_hours,
                    rating=5.0,
                    enrolled_count=0,
                    is_active=True,
                    created_at=now_utc,
                )
                session.add(new_course)
                await session.flush()

                # 3. Add default module and introductory lesson
                mod_id = f"mod_{uuid.uuid4().hex[:6]}"
                new_mod = CourseModuleModel(
                    module_id=mod_id,
                    course_id=new_id,
                    title="Module 1: Foundations & Architecture",
                    order_index=1,
                )
                session.add(new_mod)
                await session.flush()

                les_id = f"lsn_{uuid.uuid4().hex[:6]}"
                new_les = CourseLessonModel(
                    lesson_id=les_id,
                    module_id=mod_id,
                    course_id=new_id,
                    title=f"Introduction to {course_in.title}",
                    description=course_in.description[:120],
                    content=f"### {course_in.title}\n\n{course_in.description}\n\n#### Prerequisites\n- {', '.join(course_in.prerequisites) if course_in.prerequisites else 'None'}",
                    order_index=1,
                    estimated_duration_minutes=int(course_in.duration_hours * 15),
                )
                session.add(new_les)

                # 4. Map skills to course
                for s_name in course_in.prerequisites:
                    stmt_s = select(SkillModel).where(SkillModel.skill_name == s_name)
                    res_s = await session.execute(stmt_s)
                    s_obj = res_s.scalar_one_or_none()
                    if not s_obj:
                        s_obj = SkillModel(
                            skill_id=f"sk_{uuid.uuid4().hex[:6]}",
                            skill_name=s_name,
                            category=course_in.category,
                        )
                        session.add(s_obj)
                        await session.flush()
                    session.add(
                        CourseSkillModel(
                            id=f"cs_{uuid.uuid4().hex[:8]}",
                            course_id=new_id,
                            skill_id=s_obj.skill_id,
                            is_prerequisite=True,
                        )
                    )

                for s_name in course_in.skills_taught:
                    stmt_s = select(SkillModel).where(SkillModel.skill_name == s_name)
                    res_s = await session.execute(stmt_s)
                    s_obj = res_s.scalar_one_or_none()
                    if not s_obj:
                        s_obj = SkillModel(
                            skill_id=f"sk_{uuid.uuid4().hex[:6]}",
                            skill_name=s_name,
                            category=course_in.category,
                        )
                        session.add(s_obj)
                        await session.flush()
                    session.add(
                        CourseSkillModel(
                            id=f"cs_{uuid.uuid4().hex[:8]}",
                            course_id=new_id,
                            skill_id=s_obj.skill_id,
                            is_prerequisite=False,
                        )
                    )

                await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[AdminService] Create course error: {err}")
                raise

        # Update in-memory RecSys catalog immediately
        rec_course = CourseResponse(
            course_id=new_id,
            title=course_in.title,
            description=course_in.description,
            instructor_name=course_in.instructor_name,
            category=course_in.category,
            difficulty_level=course_in.difficulty_level,
            duration_hours=course_in.duration_hours,
            rating=5.0,
            enrolled_count=0,
            prerequisites=course_in.prerequisites,
            skills_taught=course_in.skills_taught,
            lessons=[
                LessonSchema(
                    lesson_id=les_id,
                    title=f"Introduction to {course_in.title}",
                    duration_minutes=int(course_in.duration_hours * 15),
                    is_completed=False,
                )
            ],
        )
        catalog_service._courses.append(rec_course)
        catalog_service._course_map[new_id] = rec_course

        await self.record_activity(
            admin_id=admin_id,
            action="COURSE_CREATED",
            target_type="course",
            target_id=new_id,
            details=f"Course '{course_in.title}' created in {course_in.category}",
        )

        return AdminCourseItem(
            course_id=new_id,
            title=course_in.title,
            description=course_in.description,
            instructor_name=course_in.instructor_name,
            category=course_in.category,
            difficulty_level=course_in.difficulty_level,
            duration_hours=course_in.duration_hours,
            rating=5.0,
            enrolled_count=0,
            is_active=True,
            prerequisites=course_in.prerequisites,
            skills_taught=course_in.skills_taught,
            modules_count=1,
            lessons_count=1,
            created_at=now_utc,
        )

    async def update_course(
        self, course_id: str, course_in: AdminCourseUpdate, admin_id: str
    ) -> Optional[AdminCourseItem]:
        """Update existing course fields and sync with AI RecSys engine."""
        async with AsyncSessionLocal() as session:
            stmt = select(CourseModel).where(CourseModel.course_id == course_id)
            res = await session.execute(stmt)
            course = res.scalar_one_or_none()
            if not course:
                return None

            if course_in.title is not None:
                course.title = course_in.title
            if course_in.description is not None:
                course.description = course_in.description
            if course_in.category is not None:
                course.category = course_in.category
            if course_in.difficulty_level is not None:
                course.difficulty_level = course_in.difficulty_level
            if course_in.duration_hours is not None:
                course.duration_hours = course_in.duration_hours
            if course_in.instructor_name is not None:
                course.instructor_name = course_in.instructor_name
            if course_in.is_active is not None:
                course.is_active = course_in.is_active

            await session.commit()

        # Update in-memory RecSys catalog
        if course_id in catalog_service._course_map:
            cached = catalog_service._course_map[course_id]
            if course_in.title is not None:
                cached.title = course_in.title
            if course_in.description is not None:
                cached.description = course_in.description
            if course_in.category is not None:
                cached.category = course_in.category
            if course_in.difficulty_level is not None:
                cached.difficulty_level = course_in.difficulty_level
            if course_in.duration_hours is not None:
                cached.duration_hours = course_in.duration_hours
            if course_in.instructor_name is not None:
                cached.instructor_name = course_in.instructor_name
            if course_in.skills_taught is not None:
                cached.skills_taught = course_in.skills_taught
            if course_in.prerequisites is not None:
                cached.prerequisites = course_in.prerequisites

        await self.record_activity(
            admin_id=admin_id,
            action="COURSE_UPDATED",
            target_type="course",
            target_id=course_id,
            details=f"Course '{course.title}' metadata updated",
        )

        courses_list = await self.list_courses()
        for c in courses_list:
            if c.course_id == course_id:
                return c
        return None

    async def update_course_status(
        self, course_id: str, is_active: bool, admin_id: str
    ) -> bool:
        """Activate or deactivate course in catalog."""
        async with AsyncSessionLocal() as session:
            stmt = select(CourseModel).where(CourseModel.course_id == course_id)
            res = await session.execute(stmt)
            course = res.scalar_one_or_none()
            if not course:
                return False
            course.is_active = is_active
            await session.commit()

        action = "COURSE_ACTIVATED" if is_active else "COURSE_DEACTIVATED"
        status_text = "activated" if is_active else "deactivated"
        await self.record_activity(
            admin_id=admin_id,
            action=action,
            target_type="course",
            target_id=course_id,
            details=f"Course '{course.title}' was {status_text} by administrator",
        )
        return True

    async def list_progress_records(
        self,
        course_id: Optional[str] = None,
        student_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[AdminProgressItem]:
        """Inspect student course progress records across the LMS."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(EnrollmentModel)
                .options(
                    selectinload(EnrollmentModel.user),
                    selectinload(EnrollmentModel.course),
                )
                .order_by(desc(EnrollmentModel.enrolled_at))
            )

            if course_id:
                stmt = stmt.where(EnrollmentModel.course_id == course_id)
            if student_id:
                stmt = stmt.where(EnrollmentModel.user_id == student_id)
            if status:
                stmt = stmt.where(EnrollmentModel.status == status)

            res = await session.execute(stmt)
            enrollments = res.scalars().all()

            results: List[AdminProgressItem] = []
            for e in enrollments:
                u = e.user
                c = e.course

                # Completed lessons count
                stmt_prog = select(func.count(ProgressModel.progress_id)).where(
                    ProgressModel.user_id == e.user_id,
                    ProgressModel.course_id == e.course_id,
                    ProgressModel.is_completed == True,
                )
                res_prog = await session.execute(stmt_prog)
                comp_count = res_prog.scalar() or 0

                # Total lessons count
                stmt_les = select(func.count(CourseLessonModel.lesson_id)).where(
                    CourseLessonModel.course_id == e.course_id
                )
                res_les = await session.execute(stmt_les)
                total_les = res_les.scalar() or 0
                if total_les == 0:
                    total_les = 4

                # Last activity timestamp
                stmt_last = select(func.max(ProgressModel.last_watched_at)).where(
                    ProgressModel.user_id == e.user_id,
                    ProgressModel.course_id == e.course_id,
                )
                res_last = await session.execute(stmt_last)
                last_act = res_last.scalar() or e.enrolled_at

                results.append(
                    AdminProgressItem(
                        enrollment_id=e.enrollment_id,
                        student_id=e.user_id,
                        student_name=u.full_name if u else "Student",
                        student_email=u.email if u else "",
                        course_id=e.course_id,
                        course_title=c.title if c else e.course_id,
                        progress_percentage=e.progress_percentage or 0.0,
                        completed_lessons=comp_count,
                        total_lessons=total_les,
                        started_date=e.enrolled_at,
                        last_activity=last_act,
                        status=e.status or "ENROLLED",
                    )
                )

            return results

    async def update_progress_record(
        self,
        enrollment_id: str,
        update_in: AdminProgressUpdate,
        admin_id: str,
    ) -> Optional[AdminProgressItem]:
        """Perform an administrative progress adjustment with required audit trail."""
        async with AsyncSessionLocal() as session:
            stmt = select(EnrollmentModel).where(EnrollmentModel.enrollment_id == enrollment_id)
            res = await session.execute(stmt)
            enr = res.scalar_one_or_none()
            if not enr:
                return None

            old_progress = enr.progress_percentage
            old_status = enr.status

            if update_in.progress_percentage is not None:
                enr.progress_percentage = max(0.0, min(100.0, update_in.progress_percentage))
                if enr.progress_percentage >= 100.0:
                    enr.status = "COMPLETED"
                    enr.completed_at = datetime.now(timezone.utc)
            if update_in.status is not None:
                enr.status = update_in.status

            await session.commit()

        await self.record_activity(
            admin_id=admin_id,
            action="PROGRESS_CORRECTED",
            target_type="progress",
            target_id=enrollment_id,
            details=(
                f"Progress updated from {old_progress}% ({old_status}) to {enr.progress_percentage}% ({enr.status}). "
                f"Reason: {update_in.reason or 'Administrative override'}"
            ),
        )

        records = await self.list_progress_records()
        for r in records:
            if r.enrollment_id == enrollment_id:
                return r
        return None

    async def get_system_analytics(self) -> AdminAnalyticsResponse:
        """Aggregate system-level student, course, learning, and skill gap metrics."""
        async with AsyncSessionLocal() as session:
            # 1. Student Analytics
            stmt_students = select(UserModel).where(UserModel.role != "admin")
            res_students = await session.execute(stmt_students)
            students = res_students.scalars().all()
            total_students = len(students)
            active_students = sum(1 for s in students if getattr(s, "is_active", True))

            now_utc = datetime.now(timezone.utc)
            thirty_days_ago = now_utc - timedelta(days=30)

            def _is_recent_registration(dt):
                if not dt:
                    return False
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt >= thirty_days_ago

            new_regs = sum(1 for s in students if _is_recent_registration(s.created_at))

            stmt_assessed = select(func.count(func.distinct(AssessmentAttemptModel.user_id)))
            res_assessed = await session.execute(stmt_assessed)
            assessed_count = res_assessed.scalar() or 0
            ass_rate = round((assessed_count / max(total_students, 1)) * 100.0, 1) if total_students > 0 else 0.0

            student_analytics = StudentAnalyticsData(
                total_students=total_students,
                new_registrations=new_regs,
                active_students=active_students,
                assessment_completion_rate=ass_rate,
            )

            # 2. Course Analytics
            stmt_courses = select(CourseModel)
            res_courses = await session.execute(stmt_courses)
            all_courses = res_courses.scalars().all()
            total_courses = len(all_courses)

            stmt_enr_all = select(EnrollmentModel)
            res_enr_all = await session.execute(stmt_enr_all)
            all_enrs = res_enr_all.scalars().all()

            enr_by_course: Dict[str, int] = {}
            comp_by_course: Dict[str, int] = {}
            for e in all_enrs:
                enr_by_course[e.course_id] = enr_by_course.get(e.course_id, 0) + 1
                if e.status == "COMPLETED" or (e.progress_percentage or 0.0) >= 100.0:
                    comp_by_course[e.course_id] = comp_by_course.get(e.course_id, 0) + 1

            course_map = {c.course_id: c.title for c in all_courses}
            for c in catalog_service._courses:
                course_map.setdefault(c.course_id, c.title)

            most_enrolled = [
                {"course_id": cid, "title": course_map.get(cid, cid), "enrollments": count}
                for cid, count in sorted(enr_by_course.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            most_completed = [
                {"course_id": cid, "title": course_map.get(cid, cid), "completions": count}
                for cid, count in sorted(comp_by_course.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            avg_comp_pct = (
                round(sum(e.progress_percentage or 0.0 for e in all_enrs) / len(all_enrs), 1)
                if all_enrs
                else 0.0
            )

            course_analytics = CourseAnalyticsData(
                total_courses=total_courses or len(catalog_service._courses),
                most_enrolled_courses=most_enrolled,
                most_completed_courses=most_completed,
                average_completion_percentage=avg_comp_pct,
            )

            # 3. Learning Analytics
            active_learners = len({e.user_id for e in all_enrs if (e.progress_percentage or 0.0) > 0})
            total_completed_courses = sum(comp_by_course.values())

            stmt_paths = select(LearningPathModel)
            res_paths = await session.execute(stmt_paths)
            all_paths = res_paths.scalars().all()
            incomplete_paths = sum(1 for p in all_paths if (p.overall_readiness or 0.0) < 100.0)

            learning_analytics = LearningAnalyticsData(
                average_student_progress=avg_comp_pct,
                active_learners_count=active_learners,
                completed_courses_count=total_completed_courses,
                incomplete_learning_paths_count=incomplete_paths,
            )

            # 4. Skill Analytics
            stmt_user_skills = select(UserSkillModel).options(selectinload(UserSkillModel.skill))
            res_user_skills = await session.execute(stmt_user_skills)
            usk_list = res_user_skills.scalars().all()

            skill_scores_sum: Dict[str, float] = {}
            skill_scores_count: Dict[str, int] = {}
            for usk in usk_list:
                s_name = usk.skill.skill_name if usk.skill else "General"
                score = (usk.mastery_score or 0.0) * 100.0 if (usk.mastery_score or 0.0) <= 1.0 else usk.mastery_score
                skill_scores_sum[s_name] = skill_scores_sum.get(s_name, 0.0) + score
                skill_scores_count[s_name] = skill_scores_count.get(s_name, 0) + 1

            skill_dist = [
                {"skill": s, "average_mastery": round(skill_scores_sum[s] / skill_scores_count[s], 1)}
                for s in sorted(skill_scores_sum.keys())
            ][:8]

            # Common skill gaps: skills with lowest average mastery
            common_gaps = [
                {
                    "skill": item["skill"],
                    "avg_gap": round(max(0.0, 80.0 - item["average_mastery"]), 1),
                    "current_mastery": item["average_mastery"],
                }
                for item in sorted(skill_dist, key=lambda x: x["average_mastery"])[:5]
            ]

            stmt_prof_goals = (
                select(ProfileModel.learning_goal, func.count(ProfileModel.profile_id))
                .group_by(ProfileModel.learning_goal)
            )
            res_prof_goals = await session.execute(stmt_prof_goals)
            goal_dist = [
                {"career_goal": row[0] or "General AI", "student_count": row[1]}
                for row in res_prof_goals.all()
            ]

            skill_analytics = SkillAnalyticsData(
                most_common_skill_gaps=common_gaps,
                skill_distribution=skill_dist,
                career_goal_distribution=goal_dist,
            )

            return AdminAnalyticsResponse(
                student_analytics=student_analytics,
                course_analytics=course_analytics,
                learning_analytics=learning_analytics,
                skill_analytics=skill_analytics,
            )

    async def get_activity_logs(self, limit: int = 50) -> List[AdminActivityItem]:
        """Fetch audit log records for administrative oversight."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(AdminActivityLogModel, UserModel)
                .outerjoin(UserModel, AdminActivityLogModel.admin_id == UserModel.user_id)
                .order_by(desc(AdminActivityLogModel.created_at))
                .limit(limit)
            )
            res = await session.execute(stmt)
            rows = res.all()

            items: List[AdminActivityItem] = []
            for log_model, user_model in rows:
                items.append(
                    AdminActivityItem(
                        log_id=log_model.log_id,
                        admin_id=log_model.admin_id,
                        admin_name=user_model.full_name if user_model else "Administrator",
                        admin_email=user_model.email if user_model else None,
                        action=log_model.action,
                        target_type=log_model.target_type,
                        target_id=log_model.target_id,
                        details=log_model.details,
                        timestamp=log_model.created_at,
                    )
                )
            return items


admin_service = AdminService()
