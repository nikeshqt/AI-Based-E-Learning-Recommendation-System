import uuid
from typing import Optional
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import UserModel, ProfileModel


class AdminSeedService:
    """Service to safely initialize or seed administrative accounts."""

    async def seed_initial_admin_if_empty(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        full_name: Optional[str] = None,
    ) -> bool:
        """Seed initial administrator account if no admin currently exists."""
        admin_email = (email or settings.DEFAULT_ADMIN_EMAIL).lower().strip()
        admin_password = password or settings.DEFAULT_ADMIN_PASSWORD
        admin_name = full_name or settings.DEFAULT_ADMIN_NAME

        async with AsyncSessionLocal() as session:
            try:
                # Check if any admin already exists
                stmt = select(UserModel).where(UserModel.role == "admin")
                res = await session.execute(stmt)
                existing_admin = res.scalar_one_or_none()

                if existing_admin:
                    return False

                # Check if the specific admin email exists as a student; if so, promote to admin
                stmt_email = select(UserModel).where(UserModel.email == admin_email)
                res_email = await session.execute(stmt_email)
                existing_by_email = res_email.scalar_one_or_none()

                if existing_by_email:
                    existing_by_email.role = "admin"
                    existing_by_email.is_active = True
                    existing_by_email.hashed_password = get_password_hash(admin_password)
                    await session.commit()
                    return True

                new_admin_id = f"usr_admin_{uuid.uuid4().hex[:8]}"
                hashed_pw = get_password_hash(admin_password)

                new_admin = UserModel(
                    user_id=new_admin_id,
                    email=admin_email,
                    hashed_password=hashed_pw,
                    full_name=admin_name,
                    role="admin",
                    is_active=True,
                )
                admin_profile = ProfileModel(
                    profile_id=f"prof_{uuid.uuid4().hex[:8]}",
                    user_id=new_admin_id,
                    learning_goal="System Administration",
                    preferred_learning_style="practical",
                    skill_level="advanced",
                )
                session.add(new_admin)
                session.add(admin_profile)
                await session.commit()
                return True
            except Exception as err:
                await session.rollback()
                print(f"[AdminSeedService] Error during admin seeding: {err}")
                return False


admin_seed_service = AdminSeedService()
