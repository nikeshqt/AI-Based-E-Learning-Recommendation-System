import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.skill import GoalRequiredSkillModel, SkillModel
from app.models.course import CourseModel, CourseSkillModel
from app.services.user_service import user_service
from app.schemas.skill_gap import SkillGapItemSchema, SkillGapResponse, SkillGapDetailResponse


DEFAULT_GOALS_MAP: Dict[str, List[Dict[str, Any]]] = {
    "Cybersecurity Analyst": [
        {"skill_name": "Python", "target_mastery": 70.0, "importance": 0.9, "is_prerequisite": False},
        {"skill_name": "Linux", "target_mastery": 75.0, "importance": 1.0, "is_prerequisite": True},
        {"skill_name": "Networking", "target_mastery": 80.0, "importance": 1.0, "is_prerequisite": True},
        {"skill_name": "Cybersecurity", "target_mastery": 85.0, "importance": 1.0, "is_prerequisite": False},
        {"skill_name": "Digital Forensics", "target_mastery": 65.0, "importance": 0.8, "is_prerequisite": False},
    ],
    "AI/ML Engineer": [
        {"skill_name": "Python", "target_mastery": 80.0, "importance": 1.0, "is_prerequisite": True},
        {"skill_name": "Machine Learning", "target_mastery": 85.0, "importance": 1.0, "is_prerequisite": False},
        {"skill_name": "Statistics", "target_mastery": 70.0, "importance": 0.9, "is_prerequisite": True},
        {"skill_name": "SQL", "target_mastery": 60.0, "importance": 0.8, "is_prerequisite": False},
        {"skill_name": "Deep Learning", "target_mastery": 80.0, "importance": 0.9, "is_prerequisite": False},
    ],
    "Data Science & AI Engineering": [
        {"skill_name": "Python", "target_mastery": 85.0, "importance": 1.0, "is_prerequisite": True},
        {"skill_name": "Data Structs", "target_mastery": 75.0, "importance": 0.9, "is_prerequisite": True},
        {"skill_name": "Machine Learning", "target_mastery": 80.0, "importance": 1.0, "is_prerequisite": False},
        {"skill_name": "SQL", "target_mastery": 80.0, "importance": 0.9, "is_prerequisite": False},
        {"skill_name": "Statistics", "target_mastery": 75.0, "importance": 0.9, "is_prerequisite": True},
    ],
    "Software Engineering": [
        {"skill_name": "Python", "target_mastery": 70.0, "importance": 0.9, "is_prerequisite": True},
        {"skill_name": "Web Development", "target_mastery": 80.0, "importance": 1.0, "is_prerequisite": False},
        {"skill_name": "SQL", "target_mastery": 75.0, "importance": 0.9, "is_prerequisite": False},
        {"skill_name": "Networking", "target_mastery": 60.0, "importance": 0.7, "is_prerequisite": False},
        {"skill_name": "Cloud Computing", "target_mastery": 70.0, "importance": 0.8, "is_prerequisite": False},
    ],
}


class SkillGapService:
    """Service providing goal-oriented skill gap calculation, prioritization, and explainable AI metadata."""

    async def seed_goal_required_skills_if_empty(self) -> None:
        """Seed PostgreSQL goal_required_skills table with default career goal target skills."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(GoalRequiredSkillModel)
                res = await session.execute(stmt)
                existing = res.scalars().all()
                if not existing:
                    for goal_name, skills_list in DEFAULT_GOALS_MAP.items():
                        for item in skills_list:
                            rec = GoalRequiredSkillModel(
                                id=f"grs_{uuid.uuid4().hex[:8]}",
                                goal_name=goal_name,
                                skill_name=item["skill_name"],
                                target_mastery=item["target_mastery"],
                                importance=item["importance"],
                                is_prerequisite=item["is_prerequisite"],
                            )
                            session.add(rec)
                    await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[SkillGapService] Seed error: {err}")

    def _get_target_skills_for_goal(self, goal_name: str) -> List[Dict[str, Any]]:
        """Retrieve target skills for specified learning goal (or fallback mapping)."""
        goal_clean = goal_name.strip()
        for g_key, items in DEFAULT_GOALS_MAP.items():
            if g_key.lower() in goal_clean.lower() or goal_clean.lower() in g_key.lower():
                return items

        # General domain fallback for custom goals
        return [
            {"skill_name": "Python", "target_mastery": 75.0, "importance": 1.0, "is_prerequisite": True},
            {"skill_name": "Networking", "target_mastery": 70.0, "importance": 0.8, "is_prerequisite": False},
            {"skill_name": "Linux", "target_mastery": 70.0, "importance": 0.8, "is_prerequisite": False},
            {"skill_name": "Cybersecurity", "target_mastery": 70.0, "importance": 0.9, "is_prerequisite": False},
            {"skill_name": "SQL", "target_mastery": 70.0, "importance": 0.8, "is_prerequisite": False},
        ]

    async def calculate_user_skill_gaps(self, user_id: str) -> SkillGapResponse:
        """Calculate authenticated user's current skill gaps against their active career goal."""
        await self.seed_goal_required_skills_if_empty()

        user = await user_service.get_by_id(user_id)
        goal = user.learning_goal if user else "Cybersecurity Analyst"

        target_skills_data = self._get_target_skills_for_goal(goal)

        # Build current user skill map (convert float 0.0-1.0 to percentage 0-100)
        current_skills_map: Dict[str, float] = {}
        if user and user.skills:
            for us in user.skills:
                m_val = us.mastery_score
                if m_val <= 1.0:
                    m_val = m_val * 100.0
                current_skills_map[us.skill_name.lower()] = round(m_val, 1)

        items: List[SkillGapItemSchema] = []
        total_current_readiness = 0.0
        total_target_readiness = 0.0

        for req in target_skills_data:
            s_name = req["skill_name"]
            target_pct = float(req["target_mastery"])
            importance = float(req.get("importance", 1.0))
            is_prereq = bool(req.get("is_prerequisite", False))

            current_pct = current_skills_map.get(s_name.lower(), 0.0)
            gap = max(round(target_pct - current_pct, 1), 0.0)

            # Priority formula: priority = min(1.0, (gap / 100) * importance * prereq_factor)
            prereq_factor = 1.25 if is_prereq else 1.0
            raw_priority = (gap / 100.0) * importance * prereq_factor
            priority = round(min(1.0, raw_priority), 2)

            if priority >= 0.35 or gap >= 35.0:
                priority_level = "High"
            elif priority >= 0.18 or gap >= 15.0:
                priority_level = "Medium"
            else:
                priority_level = "Low"

            # Categorization thresholds
            if gap == 0.0 or current_pct >= target_pct:
                category = "STRONG"
            elif gap > 45.0 or (gap > 30.0 and is_prereq):
                category = "CRITICAL_GAP"
            elif gap > 25.0:
                category = "NEEDS_IMPROVEMENT"
            else:
                category = "DEVELOPING"

            items.append(
                SkillGapItemSchema(
                    skill=s_name,
                    skill_id=f"sk_{s_name.lower()[:4]}",
                    current_mastery=current_pct,
                    target_mastery=target_pct,
                    gap=gap,
                    priority=priority,
                    priority_level=priority_level,
                    category=category,
                    is_prerequisite=is_prereq,
                    importance=importance,
                )
            )

            total_current_readiness += min(current_pct, target_pct)
            total_target_readiness += target_pct

        overall_readiness = (
            round((total_current_readiness / max(1.0, total_target_readiness)) * 100.0, 1)
            if total_target_readiness > 0
            else 100.0
        )

        # Sort skill gap items by priority descending
        items.sort(key=lambda x: x.priority, reverse=True)

        return SkillGapResponse(
            user_id=user_id,
            learning_goal=goal,
            overall_readiness=overall_readiness,
            skills=items,
        )

    async def get_skill_gap_detail(self, user_id: str, skill_id_or_name: str) -> Optional[SkillGapDetailResponse]:
        """Retrieve detailed skill gap analysis and related course mapping for a specific skill."""
        overview = await self.calculate_user_skill_gaps(user_id)
        target_item = None
        for item in overview.skills:
            if item.skill.lower() == skill_id_or_name.lower() or (item.skill_id and item.skill_id.lower() == skill_id_or_name.lower()):
                target_item = item
                break

        if not target_item:
            # Fallback if skill name not in overview
            target_item = SkillGapItemSchema(
                skill=skill_id_or_name.capitalize(),
                skill_id=f"sk_{skill_id_or_name[:4]}",
                current_mastery=35.0,
                target_mastery=75.0,
                gap=40.0,
                priority=0.45,
                priority_level="High",
                category="NEEDS_IMPROVEMENT",
                is_prerequisite=True,
                importance=1.0,
            )

        # Find related courses in PostgreSQL catalog
        related_courses: List[str] = []
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(CourseModel).join(CourseSkillModel).join(SkillModel).where(
                    SkillModel.skill_name.ilike(f"%{target_item.skill}%")
                )
                res = await session.execute(stmt)
                courses = res.scalars().all()
                related_courses = [c.title for c in courses]
            except Exception:
                pass

        if not related_courses:
            related_courses = [
                f"{target_item.skill} Fundamentals & Core Principles",
                f"Advanced {target_item.skill} Operations & Labs",
            ]

        explanation = (
            f"Your {target_item.skill} mastery is currently {int(target_item.current_mastery)}%, while your "
            f"{overview.learning_goal} goal requires approximately {int(target_item.target_mastery)}%. "
            f"Closing this {int(target_item.gap)}% gap will increase your overall career goal readiness."
        )

        prof_label = "Proficient" if target_item.current_mastery >= 70 else "Developing" if target_item.current_mastery >= 40 else "Beginner"

        return SkillGapDetailResponse(
            skill_name=target_item.skill,
            skill_id=target_item.skill_id,
            current_mastery=target_item.current_mastery,
            target_mastery=target_item.target_mastery,
            gap=target_item.gap,
            proficiency=prof_label,
            priority=target_item.priority,
            priority_level=target_item.priority_level,
            category=target_item.category,
            is_prerequisite=target_item.is_prerequisite,
            explanation=explanation,
            related_courses=related_courses,
            prerequisite_skills=["Linux"] if target_item.skill != "Linux" else ["Bash Basics"],
        )


skill_gap_service = SkillGapService()
