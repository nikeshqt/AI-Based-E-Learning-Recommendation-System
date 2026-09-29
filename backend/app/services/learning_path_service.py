import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.recommendation import LearningPathModel, LearningPathItemModel
from app.models.course import CourseModel, CourseSkillModel
from app.services.user_service import user_service
from app.services.catalog_service import catalog_service
from app.services.skill_gap_service import skill_gap_service
from app.recsys.tf_idf_engine import rec_engine
from app.schemas.user import UserResponse
from app.schemas.learning_path import (
    LearningPathResponse,
    LearningPathStageSchema,
    LearningPathItemSchema,
)


class LearningPathService:
    """Service providing real prerequisite-aware personalized learning path generation,

    transparent course priority scoring, stage grouping, PostgreSQL persistence, and ownership enforcement.
    """

    def _calculate_course_priority(
        self,
        course_skills: List[str],
        course_prereqs: List[str],
        rec_match_score: float,
        gaps_map: Dict[str, Any],
    ) -> Tuple[float, str, float, float, float, str]:
        """Compute transparent priority score and identify primary skill gap addressed by course."""
        addressed_items = []
        for s in course_skills:
            item = gaps_map.get(s.lower())
            if item:
                addressed_items.append(item)

        if addressed_items:
            # Pick primary target skill gap with highest priority
            addressed_items.sort(key=lambda x: x.priority, reverse=True)
            primary_item = addressed_items[0]
            target_skill = primary_item.skill
            gap_val = primary_item.gap
            curr_mastery = primary_item.current_mastery
            targ_mastery = primary_item.target_mastery
            importance = primary_item.importance
            is_prereq = primary_item.is_prerequisite
        else:
            target_skill = course_skills[0] if course_skills else "General AI"
            gap_val = 30.0
            curr_mastery = 40.0
            targ_mastery = 70.0
            importance = 0.8
            is_prereq = False

        # Formula: priority = 0.40*(gap/100) + 0.25*importance + 0.15*prereq + 0.10*multi_coverage + 0.10*recsys
        gap_norm = min(1.0, gap_val / 100.0)
        prereq_norm = 1.25 if is_prereq else 1.0
        multi_coverage = min(1.5, 1.0 + 0.15 * max(0, len(addressed_items) - 1))

        raw_score = (
            0.40 * gap_norm
            + 0.25 * min(1.0, importance)
            + 0.15 * prereq_norm
            + 0.10 * multi_coverage
            + 0.10 * rec_match_score
        )
        priority_score = round(min(1.0, raw_score), 3)

        if gap_val > 0:
            reason = (
                f"Addresses your {int(gap_val)}% skill gap in {target_skill} (current: {int(curr_mastery)}%, "
                f"target: {int(targ_mastery)}%). Provides key competencies for your career goal."
            )
        else:
            reason = f"Maintains high proficiency in {target_skill} and reinforces prerequisite domain knowledge."

        return priority_score, target_skill, gap_val, curr_mastery, targ_mastery, reason

    def _topological_sort_courses(
        self, courses_with_meta: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prerequisite-aware ordering algorithm ensuring prerequisite courses precede advanced courses."""
        # Map skill_name -> list of course items that TEACH this skill
        skill_teacher_map: Dict[str, List[int]] = {}
        for idx, item in enumerate(courses_with_meta):
            for s in item["course"].skills_taught:
                skill_teacher_map.setdefault(s.lower(), []).append(idx)

        # Build dependency graph
        n = len(courses_with_meta)
        in_degree = [0] * n
        adj: Dict[int, List[int]] = {i: [] for i in range(n)}

        for idx, item in enumerate(courses_with_meta):
            course = item["course"]
            for prereq in course.prerequisites:
                teachers = skill_teacher_map.get(prereq.lower(), [])
                for t_idx in teachers:
                    if t_idx != idx:
                        adj[t_idx].append(idx)
                        in_degree[idx] += 1

        # Kahn's algorithm for topological ordering
        queue = [i for i in range(n) if in_degree[i] == 0]
        # Sort queue by priority score descending to break ties
        queue.sort(key=lambda i: courses_with_meta[i]["priority_score"], reverse=True)

        ordered_indices = []
        while queue:
            curr = queue.pop(0)
            ordered_indices.append(curr)

            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
            queue.sort(key=lambda i: courses_with_meta[i]["priority_score"], reverse=True)

        # Fallback if graph contains cycles or unvisited nodes
        if len(ordered_indices) < n:
            visited = set(ordered_indices)
            remaining = [i for i in range(n) if i not in visited]
            remaining.sort(key=lambda i: courses_with_meta[i]["priority_score"], reverse=True)
            ordered_indices.extend(remaining)

        return [courses_with_meta[i] for i in ordered_indices]

    async def generate_learning_path(
        self, user_id: str, target_goal: Optional[str] = None
    ) -> LearningPathResponse:
        """Generate a personalized prerequisite-aware learning path for authenticated user."""
        user = await user_service.get_by_id(user_id)
        if not user:
            user = UserResponse(
                user_id=user_id,
                email="student@example.com",
                full_name="Student",
                learning_goal=target_goal or "Cybersecurity Analyst",
                skills=[],
            )

        if target_goal:
            await user_service.update_learning_goal(user_id, target_goal)
            user = await user_service.get_by_id(user_id)

        goal = user.learning_goal if user else "Cybersecurity Analyst"

        # Step 1: Calculate current skill gaps
        gap_overview = await skill_gap_service.calculate_user_skill_gaps(user_id)
        gaps_map = {item.skill.lower(): item for item in gap_overview.skills}

        # Step 2: Fetch courses & rank with hybrid AI engine
        all_courses = await catalog_service.list_courses()
        ranked = rec_engine.rank_courses(user=user, courses=all_courses)

        # Step 3: Compute transparent priority score for candidate courses
        courses_meta = []
        for course, match_score, rec_meta in ranked:
            p_score, target_skill, gap_val, curr_m, targ_m, reason = self._calculate_course_priority(
                course.skills_taught, course.prerequisites, match_score, gaps_map
            )
            courses_meta.append({
                "course": course,
                "match_score": match_score,
                "priority_score": p_score,
                "target_skill": target_skill,
                "gap": gap_val,
                "current_mastery": curr_m,
                "target_mastery": targ_m,
                "reason": reason,
            })

        # Step 4: Perform prerequisite-aware topological ordering
        ordered_meta = self._topological_sort_courses(courses_meta)

        # Step 5: Group ordered courses into logical stages
        total_courses_count = len(ordered_meta)
        items_by_stage: Dict[int, List[Dict[str, Any]]] = {1: [], 2: [], 3: []}

        for idx, item in enumerate(ordered_meta):
            course = item["course"]
            is_prereq_course = any(
                gaps_map.get(p.lower()) and gaps_map[p.lower()].is_prerequisite
                for p in course.skills_taught
            ) or course.difficulty_level.lower() == "beginner"

            if is_prereq_course or idx == 0:
                stage_num = 1
            elif course.difficulty_level.lower() == "advanced" or idx >= max(2, total_courses_count - 1):
                stage_num = 3
            else:
                stage_num = 2

            item["stage_number"] = stage_num
            items_by_stage[stage_num].append(item)

        stage_definitions = [
            (
                1,
                "Foundation & Prerequisites",
                "Foundation",
                "Build essential prerequisite knowledge and core technical fundamentals required for your goal.",
            ),
            (
                2,
                "Core Domain Mastery",
                "Core Skills",
                "Master primary domain competencies, hands-on operations, and applied skill frameworks.",
            ),
            (
                3,
                "Advanced Specialization",
                "Specialization",
                "Deepen expertise with advanced operational labs, architecture patterns, and specialized practices.",
            ),
        ]

        stages_schema_list: List[LearningPathStageSchema] = []
        ordered_items_schema_list: List[LearningPathItemSchema] = []
        total_duration_hours = 0.0
        global_order_idx = 1

        for stage_num, stage_title, stage_name, stage_desc in stage_definitions:
            stage_items = items_by_stage.get(stage_num, [])
            if not stage_items and stage_num != 1:
                continue

            stage_courses_schema: List[LearningPathItemSchema] = []
            stage_skills_set = set()
            stage_duration = 0.0

            for item in stage_items:
                c = item["course"]
                stage_duration += c.duration_hours
                total_duration_hours += c.duration_hours
                stage_skills_set.update(c.skills_taught)

                # Determine availability based on prerequisites
                status = "AVAILABLE" if stage_num == 1 else ("AVAILABLE" if item["match_score"] >= 0.5 else "LOCKED")

                item_schema = LearningPathItemSchema(
                    order_index=global_order_idx,
                    stage_number=stage_num,
                    stage_title=stage_title,
                    stage_name=stage_name,
                    stage_description=stage_desc,
                    course_id=c.course_id,
                    course_title=c.title,
                    target_skill=item["target_skill"],
                    skill_gap=item["gap"],
                    current_mastery=item["current_mastery"],
                    target_mastery=item["target_mastery"],
                    priority_score=item["priority_score"],
                    reason=item["reason"],
                    status=status,
                    estimated_duration_hours=c.duration_hours,
                    prerequisites=c.prerequisites,
                    skills_taught=c.skills_taught,
                )
                stage_courses_schema.append(item_schema)
                ordered_items_schema_list.append(item_schema)
                global_order_idx += 1

            stages_schema_list.append(
                LearningPathStageSchema(
                    stage_number=stage_num,
                    stage_title=stage_title,
                    stage_name=stage_name,
                    description=stage_desc,
                    target_skills=list(stage_skills_set),
                    estimated_duration_hours=round(stage_duration, 1),
                    status="AVAILABLE" if stage_num == 1 else "LOCKED",
                    courses=stage_courses_schema,
                )
            )

        # Step 6: Persist path to PostgreSQL (deactivating previous active paths)
        new_path_id = f"lp_{uuid.uuid4().hex[:10]}"
        now_utc = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as session:
            try:
                # Deactivate previous active paths for this user
                stmt_prev = select(LearningPathModel).where(
                    LearningPathModel.user_id == user_id,
                    LearningPathModel.is_active == True,
                )
                res_prev = await session.execute(stmt_prev)
                prev_paths = res_prev.scalars().all()
                for p in prev_paths:
                    p.is_active = False

                # Create new active LearningPathModel
                path_record = LearningPathModel(
                    path_id=new_path_id,
                    user_id=user_id,
                    title=f"Personalized {goal} Pathway",
                    overall_goal=goal,
                    overall_readiness=gap_overview.overall_readiness,
                    total_duration_hours=round(total_duration_hours, 1),
                    total_duration_weeks=max(1, int(round(total_duration_hours / 4.0))),
                    is_active=True,
                    created_at=now_utc,
                )
                session.add(path_record)

                # Create associated LearningPathItemModel records
                for item in ordered_items_schema_list:
                    item_rec = LearningPathItemModel(
                        item_id=f"lpi_{uuid.uuid4().hex[:10]}",
                        path_id=new_path_id,
                        order_index=item.order_index,
                        stage_number=item.stage_number,
                        stage_title=item.stage_title,
                        stage_name=item.stage_name,
                        stage_description=item.stage_description,
                        course_id=item.course_id,
                        target_skill=item.target_skill,
                        skill_gap=item.skill_gap,
                        current_mastery=item.current_mastery,
                        target_mastery=item.target_mastery,
                        priority_score=item.priority_score,
                        reason=item.reason,
                        status=item.status,
                        estimated_duration_hours=item.estimated_duration_hours,
                        estimated_weeks=max(1, int(round(item.estimated_duration_hours / 2.0))),
                    )
                    session.add(item_rec)

                await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[LearningPathService] PostgreSQL persistence error: {err}")

        return LearningPathResponse(
            learning_path_id=new_path_id,
            user_id=user_id,
            career_goal=goal,
            overall_readiness=gap_overview.overall_readiness,
            total_duration_hours=round(total_duration_hours, 1),
            total_stages=len(stages_schema_list),
            total_courses=len(ordered_items_schema_list),
            generated_at=now_utc,
            is_active=True,
            stages=stages_schema_list,
            ordered_courses=ordered_items_schema_list,
        )

    async def get_active_path_for_user(self, user_id: str) -> Optional[LearningPathResponse]:
        """Retrieve active learning path for user from PostgreSQL, or generate if none exists."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(LearningPathModel)
                .options(
                    selectinload(LearningPathModel.items)
                    .selectinload(LearningPathItemModel.course)
                    .selectinload(CourseModel.course_skills)
                    .selectinload(CourseSkillModel.skill)
                )
                .where(
                    LearningPathModel.user_id == user_id,
                    LearningPathModel.is_active == True,
                )
                .order_by(LearningPathModel.created_at.desc())
            )
            res = await session.execute(stmt)
            path_model = res.scalars().first()

        if not path_model:
            # Generate initial learning path if none exists
            return await self.generate_learning_path(user_id)

        # Build stages and items from persisted PostgreSQL record
        return await self._build_response_from_model(path_model)

    async def get_path_by_id(self, path_id: str, current_user_id: str) -> Tuple[Optional[LearningPathResponse], bool]:
        """Retrieve specific learning path by ID and enforce strict user authorization."""
        async with AsyncSessionLocal() as session:
            stmt = (
                select(LearningPathModel)
                .options(
                    selectinload(LearningPathModel.items)
                    .selectinload(LearningPathItemModel.course)
                    .selectinload(CourseModel.course_skills)
                    .selectinload(CourseSkillModel.skill)
                )
                .where(LearningPathModel.path_id == path_id)
            )
            res = await session.execute(stmt)
            path_model = res.scalars().first()

        if not path_model:
            return None, True  # Authorized, but not found

        if path_model.user_id != current_user_id:
            return None, False  # Unauthorized (Forbidden)

        response = await self._build_response_from_model(path_model)
        return response, True

    async def _build_response_from_model(self, path_model: LearningPathModel) -> LearningPathResponse:
        """Helper to convert LearningPathModel ORM entity to LearningPathResponse schema."""
        sorted_items = sorted(path_model.items, key=lambda x: x.order_index)

        items_schema: List[LearningPathItemSchema] = []
        stages_dict: Dict[int, List[LearningPathItemSchema]] = {}

        for item in sorted_items:
            course = item.course
            prereqs = []
            if course and "course_skills" in course.__dict__:
                prereqs = course.__dict__.get("course_skills") or []
            skills_t = [cs.skill.skill_name for cs in prereqs if cs.skill and not cs.is_prerequisite] if prereqs else []
            prereq_s = [cs.skill.skill_name for cs in prereqs if cs.skill and cs.is_prerequisite] if prereqs else []

            item_schema = LearningPathItemSchema(
                item_id=item.item_id,
                path_id=item.path_id,
                order_index=item.order_index,
                stage_number=item.stage_number,
                stage_title=item.stage_title,
                stage_name=item.stage_name,
                stage_description=item.stage_description,
                course_id=item.course_id,
                course_title=course.title if course else item.course_id,
                target_skill=item.target_skill or "Core Domain",
                skill_gap=item.skill_gap,
                current_mastery=item.current_mastery,
                target_mastery=item.target_mastery,
                priority_score=item.priority_score,
                reason=item.reason or "Required step in personalized learning path.",
                status=item.status or "AVAILABLE",
                estimated_duration_hours=item.estimated_duration_hours or (course.duration_hours if course else 4.0),
                prerequisites=prereq_s or ["Linux"],
                skills_taught=skills_t or [item.target_skill],
            )
            items_schema.append(item_schema)
            stages_dict.setdefault(item.stage_number, []).append(item_schema)

        stages_schema: List[LearningPathStageSchema] = []
        stage_names_map = {
            1: ("Foundation & Prerequisites", "Foundation", "Build essential prerequisite knowledge and core technical fundamentals."),
            2: ("Core Domain Mastery", "Core Skills", "Master primary domain competencies, hands-on operations, and applied skill frameworks."),
            3: ("Advanced Specialization", "Specialization", "Deepen expertise with advanced operational labs, architecture patterns, and specialized practices."),
        }

        for st_num in sorted(stages_dict.keys()):
            st_courses = stages_dict[st_num]
            st_title, st_name, st_desc = stage_names_map.get(
                st_num, (f"Stage {st_num}", f"Stage {st_num}", "Learning path stage")
            )
            st_dur = sum(c.estimated_duration_hours for c in st_courses)
            st_skills = list({s for c in st_courses for s in c.skills_taught})

            stages_schema.append(
                LearningPathStageSchema(
                    stage_number=st_num,
                    stage_title=st_title,
                    stage_name=st_name,
                    description=st_desc,
                    target_skills=st_skills,
                    estimated_duration_hours=round(st_dur, 1),
                    status="AVAILABLE" if st_num == 1 else "LOCKED",
                    courses=st_courses,
                )
            )

        return LearningPathResponse(
            learning_path_id=path_model.path_id,
            user_id=path_model.user_id,
            career_goal=path_model.overall_goal,
            overall_readiness=path_model.overall_readiness,
            total_duration_hours=path_model.total_duration_hours,
            total_stages=len(stages_schema),
            total_courses=len(items_schema),
            generated_at=path_model.created_at or datetime.now(timezone.utc),
            is_active=path_model.is_active,
            stages=stages_schema,
            ordered_courses=items_schema,
        )


learning_path_service = LearningPathService()
