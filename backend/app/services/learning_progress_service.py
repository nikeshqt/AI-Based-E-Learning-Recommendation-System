import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.course import CourseModel, CourseModuleModel, CourseLessonModel
from app.models.learning import EnrollmentModel, ProgressModel
from app.schemas.learning_progress import (
    EnrollmentResponse,
    LessonPublicSchema,
    ModulePublicSchema,
    CourseLearningResponse,
    LessonCompleteResponse,
    ContinueLearningResponse,
    DashboardStatsResponse,
)


class LearningProgressService:
    """Service handling course enrollment, educational lesson content seeding,

    backend progress percentage calculation, lesson completion, continue learning, and dashboard stats.
    """

    async def seed_course_content_if_empty(self) -> None:
        """Seed PostgreSQL course_modules and course_lessons with educational demo content."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(CourseModuleModel)
                res = await session.execute(stmt)
                existing = res.scalars().all()
                if existing:
                    return

                # Sample Course 1: Advanced Cybersecurity Analysis & Network Defense (crs_sec_04)
                mod_sec_1 = CourseModuleModel(
                    module_id="mod_sec_1",
                    course_id="crs_sec_04",
                    title="Linux Security & Kernel Auditing",
                    order_index=1,
                )
                session.add(mod_sec_1)

                les_sec_1 = CourseLessonModel(
                    lesson_id="lsn_sec_1",
                    module_id="mod_sec_1",
                    course_id="crs_sec_04",
                    title="Introduction to Linux Hardening & Auditd",
                    description="Learn Linux kernel audit parameters, log monitoring, and file permission checks.",
                    content="""### Linux Kernel Hardening & Auditd Overview

Linux system auditing allows security analysts to track system calls, file access, and user privilege escalation.

#### Key Principles:
1. **File System Integrity**: Monitor sensitive files like `/etc/passwd` and `/etc/sudoers`.
2. **Audit Rules Setup**: Configure `/etc/audit/audit.rules` to capture execve system calls.
3. **Privilege Control**: Restrict `sudo` access and disable root SSH login (`PermitRootLogin no`).

Use auditctl to verify active rules:
```bash
auditctl -l
```""",
                    order_index=1,
                    estimated_duration_minutes=20,
                )
                les_sec_2 = CourseLessonModel(
                    lesson_id="lsn_sec_2",
                    module_id="mod_sec_1",
                    course_id="crs_sec_04",
                    title="File System Security & ACL Permission Control",
                    description="Configure POSIX Access Control Lists and setuid bit restrictions.",
                    content="""### File System Security & Access Control Lists (ACLs)

Standard Linux permissions (rwx) can be extended using POSIX Access Control Lists (ACLs).

#### Important Commands:
- `getfacl filename`: Inspect ACL entries for a file.
- `setfacl -m u:analyst:rwx filename`: Grant user 'analyst' explicit read-write-execute permissions.
- Disable unsafe SUID binaries to prevent privilege escalation exploits.""",
                    order_index=2,
                    estimated_duration_minutes=25,
                )
                session.add_all([les_sec_1, les_sec_2])

                mod_sec_2 = CourseModuleModel(
                    module_id="mod_sec_2",
                    course_id="crs_sec_04",
                    title="Network Security Operations & Packet Analysis",
                    order_index=2,
                )
                session.add(mod_sec_2)

                les_sec_3 = CourseLessonModel(
                    lesson_id="lsn_sec_3",
                    module_id="mod_sec_2",
                    course_id="crs_sec_04",
                    title="Wireshark Packet Inspection & Intrusion Detection",
                    description="Analyze pcap traces to identify network scanning, ARP spoofing, and malicious payloads.",
                    content="""### Wireshark Packet Inspection

Packet inspection reveals malicious traffic patterns, unencrypted authentication credentials, and anomalous network sweeps.

#### Display Filters:
- `ip.addr == 192.168.1.1`: Filter traffic for a specific target host.
- `tcp.flags.syn == 1 and tcp.flags.ack == 0`: Identify SYN flood port scans.
- `http.request.method == "POST"`: Inspect web form submissions.""",
                    order_index=3,
                    estimated_duration_minutes=30,
                )
                les_sec_4 = CourseLessonModel(
                    lesson_id="lsn_sec_4",
                    module_id="mod_sec_2",
                    course_id="crs_sec_04",
                    title="Python Automation for Threat Vector Remediation",
                    description="Automate IP blocking and firewall rule updates using Python scripts.",
                    content="""### Automated Threat Remediation

Python scripts can interface with iptables or firewall APIs to auto-block offending IP addresses detected by SIEM logs.

#### Script Workflow:
1. Parse log streams for repeated failed authentication attempts.
2. Extract offending IP addresses.
3. Execute `subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])`.""",
                    order_index=4,
                    estimated_duration_minutes=35,
                )
                session.add_all([les_sec_3, les_sec_4])

                # Sample Course 2: Production Vector Search with Qdrant (crs_qdrant_02)
                mod_qd_1 = CourseModuleModel(
                    module_id="mod_qd_1",
                    course_id="crs_qdrant_02",
                    title="Vector Databases & HNSW Indexing",
                    order_index=1,
                )
                session.add(mod_qd_1)

                les_qd_1 = CourseLessonModel(
                    lesson_id="lsn_qd_1",
                    module_id="mod_qd_1",
                    course_id="crs_qdrant_02",
                    title="Introduction to High-Dimensional Vector Embeddings",
                    description="Understand vector embeddings, cosine distance, and dense retrieval.",
                    content="""### High-Dimensional Vector Embeddings

Dense vector embeddings map unstructured data (text, images) into a continuous vector space where semantic similarity corresponds to geometric distance.

#### Key Concepts:
- **Cosine Distance**: Measures similarity between vector directions regardless of magnitude.
- **Euclidean Distance (L2)**: Measures straight-line distance between vector endpoints.
- **Inner Product (Dot)**: Fast similarity metric for normalized unit vectors.""",
                    order_index=1,
                    estimated_duration_minutes=20,
                )
                les_qd_2 = CourseLessonModel(
                    lesson_id="lsn_qd_2",
                    module_id="mod_qd_1",
                    course_id="crs_qdrant_02",
                    title="HNSW Graph Indexing & Nearest Neighbor Search",
                    description="Master Hierarchical Navigable Small World graphs for fast ANN retrieval.",
                    content="""### HNSW Graph Indexing

Hierarchical Navigable Small World (HNSW) graphs organize vectors into multi-layer skip-list graphs to achieve logarithmic time search ($O(\log N)$).

#### Parameters:
- `m`: Maximum number of outgoing links per node.
- `ef_construct`: Size of dynamic candidate list during index construction.
- `ef_search`: Candidate list size during query execution.""",
                    order_index=2,
                    estimated_duration_minutes=25,
                )
                session.add_all([les_qd_1, les_qd_2])

                await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[LearningProgressService] Seed error: {err}")

    async def enroll_user(self, user_id: str, course_id: str) -> EnrollmentResponse:
        """Enroll student in course, returning existing enrollment if already enrolled."""
        async with AsyncSessionLocal() as session:
            stmt = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.course_id == course_id,
            )
            res = await session.execute(stmt)
            existing = res.scalars().first()

            if existing:
                return EnrollmentResponse.model_validate(existing)

            new_enrollment = EnrollmentModel(
                enrollment_id=f"enr_{uuid.uuid4().hex[:10]}",
                user_id=user_id,
                course_id=course_id,
                status="ENROLLED",
                progress_percentage=0.0,
                enrolled_at=datetime.now(timezone.utc),
            )
            session.add(new_enrollment)
            await session.commit()
            await session.refresh(new_enrollment)
            return EnrollmentResponse.model_validate(new_enrollment)

    async def get_course_learning_content(
        self, user_id: str, course_id: str
    ) -> CourseLearningResponse:
        """Retrieve course modules, lessons, and student completion status."""
        await self.seed_course_content_if_empty()

        async with AsyncSessionLocal() as session:
            # Check enrollment status
            stmt_enr = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.course_id == course_id,
            )
            res_enr = await session.execute(stmt_enr)
            enrollment = res_enr.scalars().first()
            status = enrollment.status if enrollment else "NOT_STARTED"

            # Check completed lessons in ProgressModel
            stmt_prog = select(ProgressModel).where(
                ProgressModel.user_id == user_id,
                ProgressModel.course_id == course_id,
                ProgressModel.is_completed == True,
            )
            res_prog = await session.execute(stmt_prog)
            completed_lesson_ids = {p.lesson_id for p in res_prog.scalars().all()}

            # Fetch course title & metadata
            stmt_course = (
                select(CourseModel)
                .options(
                    selectinload(CourseModel.modules).selectinload(CourseModuleModel.lessons)
                )
                .where(CourseModel.course_id == course_id)
            )
            res_course = await session.execute(stmt_course)
            course = res_course.scalars().first()

            if not course:
                # Demo course fallback metadata if course_id not in DB catalog
                course_title = "Advanced Cybersecurity Analysis & Network Defense"
                category = "Cybersecurity"
                difficulty = "Intermediate"
                duration = 8.0
            else:
                course_title = course.title
                category = course.category
                difficulty = course.difficulty_level
                duration = course.duration_hours

            # Fetch modules and lessons
            stmt_mods = (
                select(CourseModuleModel)
                .options(selectinload(CourseModuleModel.lessons))
                .where(CourseModuleModel.course_id == course_id)
                .order_by(CourseModuleModel.order_index)
            )
            res_mods = await session.execute(stmt_mods)
            modules_db = res_mods.scalars().all()

            modules_schema: List[ModulePublicSchema] = []
            total_lessons_count = 0

            if modules_db:
                for mod in modules_db:
                    lessons_schema: List[LessonPublicSchema] = []
                    sorted_lessons = sorted(mod.lessons, key=lambda x: x.order_index)
                    for les in sorted_lessons:
                        total_lessons_count += 1
                        is_comp = les.lesson_id in completed_lesson_ids
                        lessons_schema.append(
                            LessonPublicSchema(
                                lesson_id=les.lesson_id,
                                module_id=les.module_id,
                                course_id=les.course_id,
                                title=les.title,
                                description=les.description,
                                content=les.content,
                                order_index=les.order_index,
                                estimated_duration_minutes=les.estimated_duration_minutes,
                                is_completed=is_comp,
                            )
                        )
                    modules_schema.append(
                        ModulePublicSchema(
                            module_id=mod.module_id,
                            course_id=mod.course_id,
                            title=mod.title,
                            order_index=mod.order_index,
                            lessons=lessons_schema,
                        )
                    )

            if total_lessons_count == 0:
                # Default demo module/lesson fallback
                total_lessons_count = 4
                default_lessons = [
                    LessonPublicSchema(
                        lesson_id="lsn_sec_1",
                        module_id="mod_sec_1",
                        course_id=course_id,
                        title="Introduction to Linux Hardening & Auditd",
                        description="Learn Linux kernel audit parameters and log monitoring.",
                        content="### Linux Security Architecture\n\nConfigure auditctl rules.",
                        order_index=1,
                        estimated_duration_minutes=20,
                        is_completed="lsn_sec_1" in completed_lesson_ids,
                    ),
                    LessonPublicSchema(
                        lesson_id="lsn_sec_2",
                        module_id="mod_sec_1",
                        course_id=course_id,
                        title="File System Security & ACL Control",
                        description="Configure POSIX Access Control Lists.",
                        content="### ACL Permissions\n\nUse setfacl to manage permissions.",
                        order_index=2,
                        estimated_duration_minutes=25,
                        is_completed="lsn_sec_2" in completed_lesson_ids,
                    ),
                ]
                modules_schema = [
                    ModulePublicSchema(
                        module_id="mod_sec_1",
                        course_id=course_id,
                        title="Linux Security Fundamentals",
                        order_index=1,
                        lessons=default_lessons,
                    )
                ]

            completed_count = len(completed_lesson_ids)
            progress_pct = round((completed_count / max(1, total_lessons_count)) * 100.0, 1)

            return CourseLearningResponse(
                course_id=course_id,
                title=course_title,
                category=category,
                difficulty_level=difficulty,
                duration_hours=duration,
                status=status,
                progress_percentage=progress_pct,
                completed_lessons_count=completed_count,
                total_lessons_count=total_lessons_count,
                modules=modules_schema,
            )

    async def complete_lesson(
        self, user_id: str, course_id: str, lesson_id: str
    ) -> LessonCompleteResponse:
        """Mark lesson complete, update backend progress %, and set enrollment to COMPLETED if all done."""
        async with AsyncSessionLocal() as session:
            # Auto-enroll user if not enrolled
            stmt_enr = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.course_id == course_id,
            )
            res_enr = await session.execute(stmt_enr)
            enrollment = res_enr.scalars().first()

            if not enrollment:
                enrollment = EnrollmentModel(
                    enrollment_id=f"enr_{uuid.uuid4().hex[:10]}",
                    user_id=user_id,
                    course_id=course_id,
                    status="IN_PROGRESS",
                    progress_percentage=0.0,
                    enrolled_at=datetime.now(timezone.utc),
                )
                session.add(enrollment)

            # Record lesson completion in ProgressModel
            stmt_prog = select(ProgressModel).where(
                ProgressModel.user_id == user_id,
                ProgressModel.course_id == course_id,
                ProgressModel.lesson_id == lesson_id,
            )
            res_prog = await session.execute(stmt_prog)
            existing_prog = res_prog.scalars().first()

            if not existing_prog:
                prog_record = ProgressModel(
                    progress_id=f"prg_{uuid.uuid4().hex[:10]}",
                    user_id=user_id,
                    course_id=course_id,
                    lesson_id=lesson_id,
                    is_completed=True,
                    last_watched_at=datetime.now(timezone.utc),
                )
                session.add(prog_record)
            else:
                existing_prog.is_completed = True

            await session.commit()

        # Calculate updated backend progress percentage
        learning_content = await self.get_course_learning_content(user_id, course_id)
        progress_pct = learning_content.progress_percentage
        is_finished = (
            learning_content.completed_lessons_count >= learning_content.total_lessons_count
            and learning_content.total_lessons_count > 0
        )

        async with AsyncSessionLocal() as session:
            stmt_enr2 = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.course_id == course_id,
            )
            res_enr2 = await session.execute(stmt_enr2)
            enr2 = res_enr2.scalars().first()

            if enr2:
                enr2.progress_percentage = progress_pct
                if is_finished:
                    enr2.status = "COMPLETED"
                    enr2.completed_at = datetime.now(timezone.utc)
                else:
                    enr2.status = "IN_PROGRESS"
                await session.commit()

        return LessonCompleteResponse(
            lesson_id=lesson_id,
            course_id=course_id,
            is_completed=True,
            progress_percentage=progress_pct,
            course_completed=is_finished,
            status="COMPLETED" if is_finished else "IN_PROGRESS",
        )

    async def get_continue_learning(self, user_id: str) -> ContinueLearningResponse:
        """Retrieve most relevant active course & next incomplete lesson for user."""
        await self.seed_course_content_if_empty()

        async with AsyncSessionLocal() as session:
            stmt = (
                select(EnrollmentModel)
                .where(
                    EnrollmentModel.user_id == user_id,
                    EnrollmentModel.status.in_(["ENROLLED", "IN_PROGRESS"]),
                    EnrollmentModel.progress_percentage < 100.0,
                )
                .order_by(EnrollmentModel.enrolled_at.desc())
            )
            res = await session.execute(stmt)
            active_enr = res.scalars().first()

        if not active_enr:
            return ContinueLearningResponse(has_active_course=False)

        content = await self.get_course_learning_content(user_id, active_enr.course_id)

        # Find first incomplete lesson
        next_les = None
        for mod in content.modules:
            for les in mod.lessons:
                if not les.is_completed:
                    next_les = les
                    break
            if next_les:
                break

        if not next_les:
            return ContinueLearningResponse(
                has_active_course=True,
                course_id=content.course_id,
                course_title=content.title,
                progress_percentage=content.progress_percentage,
                next_lesson_id=None,
                next_lesson_title="Course Complete",
                estimated_duration_minutes=0,
            )

        return ContinueLearningResponse(
            has_active_course=True,
            course_id=content.course_id,
            course_title=content.title,
            progress_percentage=content.progress_percentage,
            next_lesson_id=next_les.lesson_id,
            next_lesson_title=next_les.title,
            estimated_duration_minutes=next_les.estimated_duration_minutes,
        )

    async def get_dashboard_stats(self, user_id: str) -> DashboardStatsResponse:
        """Retrieve counts of completed & in-progress courses plus active continue learning payload."""
        async with AsyncSessionLocal() as session:
            stmt_comp = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.status == "COMPLETED",
            )
            res_comp = await session.execute(stmt_comp)
            completed_count = len(res_comp.scalars().all())

            stmt_prog = select(EnrollmentModel).where(
                EnrollmentModel.user_id == user_id,
                EnrollmentModel.status.in_(["ENROLLED", "IN_PROGRESS"]),
                EnrollmentModel.progress_percentage < 100.0,
            )
            res_prog = await session.execute(stmt_prog)
            in_prog_count = len(res_prog.scalars().all())

        continue_payload = await self.get_continue_learning(user_id)

        return DashboardStatsResponse(
            completed_courses_count=completed_count,
            in_progress_courses_count=in_prog_count,
            continue_learning=continue_payload,
        )


learning_progress_service = LearningProgressService()
