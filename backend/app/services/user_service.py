from typing import Optional, Dict, Any, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash, verify_password
from app.models.user import UserModel, ProfileModel
from app.models.skill import SkillModel, UserSkillModel
from app.schemas.user import UserCreate, UserResponse, SkillMasterySchema
from datetime import datetime, timezone
from fastapi import HTTPException, status


class UserService:
    """User Management Service providing persistent account creation, auth, and profile management."""

    def __init__(self):
        demo_hashed_pw = get_password_hash("password123")
        self._demo_dict = {
            "user_id": "usr_98741",
            "email": "alex.morgan@ai-learning.io",
            "full_name": "Alex Morgan",
            "hashed_password": demo_hashed_pw,
            "learning_goal": "Data Science & AI Engineering",
            "preferred_learning_style": "visual",
            "skill_level": "intermediate",
            "role": "student",
            "is_active": True,
            "weekly_goal_hours": 5,
            "completed_hours": 4.2,
            "streak_days": 12,
            "skills": [
                {
                    "skill_id": "sk_py",
                    "skill_name": "Python",
                    "mastery_score": 0.85,
                    "last_evaluated": datetime.now(timezone.utc),
                    "category": "Programming",
                },
                {
                    "skill_id": "sk_ds",
                    "skill_name": "Data Structs",
                    "mastery_score": 0.75,
                    "last_evaluated": datetime.now(timezone.utc),
                    "category": "CS Core",
                },
            ],
        }
        self._demo_user2 = {
            **self._demo_dict,
            "user_id": "usr_demo",
            "email": "demo@ai-learning.io",
            "full_name": "Demo Student",
            "learning_goal": "Cybersecurity Analyst",
        }
        self._memory_users: Dict[str, Dict[str, Any]] = {
            "alex.morgan@ai-learning.io": self._demo_dict,
            "demo@ai-learning.io": self._demo_user2,
        }

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user dictionary by email address."""
        email_clean = email.lower().strip()
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(UserModel).options(selectinload(UserModel.profile)).where(UserModel.email == email_clean)
                result = await session.execute(stmt)
                user_obj = result.scalar_one_or_none()
                if user_obj:
                    return {
                        "user_id": user_obj.user_id,
                        "email": user_obj.email,
                        "full_name": user_obj.full_name,
                        "hashed_password": user_obj.hashed_password,
                        "role": getattr(user_obj, "role", "student"),
                        "is_active": getattr(user_obj, "is_active", True),
                        "last_login": user_obj.last_login,
                        "created_at": user_obj.created_at,
                        "learning_goal": user_obj.profile.learning_goal if user_obj.profile else "General AI",
                    }
            except Exception:
                pass
        return self._memory_users.get(email_clean)

    async def get_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Retrieve user profile response by ID."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(UserModel).options(
                    selectinload(UserModel.profile),
                    selectinload(UserModel.skills).selectinload(UserSkillModel.skill)
                ).where(UserModel.user_id == user_id)
                result = await session.execute(stmt)
                user_obj = result.scalar_one_or_none()
                if user_obj:
                    skills_list = []
                    for us in user_obj.skills:
                        skills_list.append(
                            SkillMasterySchema(
                                skill_id=us.skill_id,
                                skill_name=us.skill.skill_name if us.skill else us.skill_id,
                                mastery_score=us.mastery_score,
                                last_evaluated=us.last_evaluated,
                                category=us.skill.category if us.skill else "Domain Skill",
                            )
                        )
                    prof = user_obj.profile
                    return UserResponse(
                        user_id=user_obj.user_id,
                        email=user_obj.email,
                        full_name=user_obj.full_name,
                        role=getattr(user_obj, "role", "student"),
                        is_active=getattr(user_obj, "is_active", True),
                        last_login=user_obj.last_login,
                        created_at=user_obj.created_at,
                        learning_goal=prof.learning_goal if prof else "General AI",
                        preferred_learning_style=prof.preferred_learning_style if prof else "visual",
                        skill_level=prof.skill_level if prof else "beginner",
                        weekly_goal_hours=prof.weekly_goal_hours if prof else 5,
                        completed_hours=prof.completed_hours if prof else 0.0,
                        streak_days=prof.streak_days if prof else 1,
                        skills=skills_list,
                    )
            except Exception:
                pass

        # Memory fallback search
        for u in self._memory_users.values():
            if u["user_id"] == user_id:
                return UserResponse(**u)
        return None

    async def create_user(self, user_in: UserCreate, role: str = "student") -> UserResponse:
        """Register a new user account with persistent profile."""
        existing = await self.get_by_email(user_in.email)
        if existing:
            raise ValueError("User with this email already exists")

        new_id = f"usr_{uuid.uuid4().hex[:8]}"
        email_clean = user_in.email.lower().strip()
        hashed_pw = get_password_hash(user_in.password)

        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    user_obj = UserModel(
                        user_id=new_id,
                        email=email_clean,
                        full_name=user_in.full_name,
                        hashed_password=hashed_pw,
                        role=role,
                        is_active=True,
                    )
                    profile_obj = ProfileModel(
                        profile_id=f"prof_{uuid.uuid4().hex[:8]}",
                        user_id=new_id,
                        learning_goal=user_in.learning_goal,
                        preferred_learning_style=user_in.preferred_learning_style,
                        skill_level=user_in.skill_level,
                    )
                    session.add(user_obj)
                    session.add(profile_obj)
                    await session.commit()
            except Exception:
                await session.rollback()

        user_dict = {
            "user_id": new_id,
            "email": email_clean,
            "full_name": user_in.full_name,
            "hashed_password": hashed_pw,
            "role": role,
            "is_active": True,
            "learning_goal": user_in.learning_goal,
            "preferred_learning_style": user_in.preferred_learning_style,
            "skill_level": user_in.skill_level,
            "weekly_goal_hours": 5,
            "completed_hours": 0.0,
            "streak_days": 1,
            "skills": [],
        }
        self._memory_users[email_clean] = user_dict
        return UserResponse(**user_dict)

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Validate credentials for user login and update last_login timestamp."""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Please contact an administrator.",
            )

        now_utc = datetime.now(timezone.utc)
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(UserModel).where(UserModel.user_id == user["user_id"])
                res = await session.execute(stmt)
                u_obj = res.scalar_one_or_none()
                if u_obj:
                    u_obj.last_login = now_utc
                    await session.commit()
            except Exception:
                pass

        user["last_login"] = now_utc

        # Record audit log if admin logs in
        if user.get("role") == "admin":
            try:
                from app.models.admin_log import AdminActivityLogModel
                async with AsyncSessionLocal() as session:
                    log_entry = AdminActivityLogModel(
                        log_id=f"log_{uuid.uuid4().hex[:10]}",
                        admin_id=user["user_id"],
                        action="ADMIN_LOGIN",
                        target_type="auth",
                        target_id=user["user_id"],
                        details=f"Admin {user.get('full_name')} logged in successfully",
                    )
                    session.add(log_entry)
                    await session.commit()
            except Exception as log_err:
                print(f"[UserService] Warning logging admin login: {log_err}")

        return user

    async def update_user_status(self, user_id: str, is_active: bool) -> bool:
        """Activate or deactivate student account."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(UserModel).where(UserModel.user_id == user_id)
                res = await session.execute(stmt)
                user_obj = res.scalar_one_or_none()
                if not user_obj:
                    return False
                user_obj.is_active = is_active
                await session.commit()

                # Also update in memory if present
                for u in self._memory_users.values():
                    if u.get("user_id") == user_id:
                        u["is_active"] = is_active
                return True
            except Exception as err:
                await session.rollback()
                print(f"[UserService] update_user_status error: {err}")
                return False

    async def update_learning_goal(self, user_id: str, new_goal: str) -> Optional[UserResponse]:
        """Update user target learning goal."""
        return await self.update_user_profile(user_id=user_id, learning_goal=new_goal)

    async def update_user_profile(
        self,
        user_id: str,
        learning_goal: Optional[str] = None,
        skills: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[UserResponse]:
        """Update learner profile skills and goals in database."""
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    stmt = select(ProfileModel).where(ProfileModel.user_id == user_id)
                    result = await session.execute(stmt)
                    prof = result.scalar_one_or_none()
                    if prof and learning_goal:
                        prof.learning_goal = learning_goal

                    if skills is not None:
                        now_utc = datetime.now(timezone.utc)
                        for idx, sk in enumerate(skills):
                            s_name = sk.get("skill_name")
                            if not s_name:
                                continue
                            m_score = float(sk.get("mastery_score", 0.0))
                            # Normalize score if 0-100 scale passed
                            if m_score > 1.0:
                                m_score = m_score / 100.0

                            stmt_sk = select(SkillModel).where(SkillModel.skill_name == s_name)
                            res_sk = await session.execute(stmt_sk)
                            sk_obj = res_sk.scalar_one_or_none()
                            if not sk_obj:
                                sk_obj = SkillModel(
                                    skill_id=f"sk_{uuid.uuid4().hex[:6]}",
                                    skill_name=s_name,
                                    category=sk.get("category", "Domain Skill"),
                                    description=f"{s_name} Skill",
                                )
                                session.add(sk_obj)
                                await session.flush()

                            stmt_us = select(UserSkillModel).where(
                                UserSkillModel.user_id == user_id,
                                UserSkillModel.skill_id == sk_obj.skill_id
                            )
                            res_us = await session.execute(stmt_us)
                            us_obj = res_us.scalar_one_or_none()
                            if us_obj:
                                us_obj.mastery_score = max(us_obj.mastery_score or 0.0, m_score)
                                us_obj.last_evaluated = now_utc
                            else:
                                new_us = UserSkillModel(
                                    id=f"usk_{uuid.uuid4().hex[:8]}",
                                    user_id=user_id,
                                    skill_id=sk_obj.skill_id,
                                    mastery_score=m_score,
                                    last_evaluated=now_utc,
                                )
                                session.add(new_us)
                    await session.commit()
            except Exception as err:
                await session.rollback()
                print(f"[UserService] Profile update error: {err}")

        # Update memory store representation
        for u in self._memory_users.values():
            if u["user_id"] == user_id:
                if learning_goal:
                    u["learning_goal"] = learning_goal
                if skills is not None:
                    formatted_skills = []
                    for idx, sk in enumerate(skills):
                        m_val = float(sk.get("mastery_score", 0.0))
                        if m_val > 1.0:
                            m_val = m_val / 100.0
                        formatted_skills.append({
                            "skill_id": f"sk_{idx+1}",
                            "skill_name": sk.get("skill_name"),
                            "mastery_score": m_val,
                            "last_evaluated": datetime.now(timezone.utc),
                            "category": sk.get("category", "Domain Skill"),
                        })
                    u["skills"] = formatted_skills

        return await self.get_by_id(user_id)


user_service = UserService()
