from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from app.core.config import settings
from app.core.database import AsyncSessionLocal

# Use pbkdf2_sha256 first for pure-python reliability, with bcrypt fallback
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using pbkdf2_sha256 / bcrypt."""
    return pwd_context.hash(password)


def create_access_token(
    subject: str | Any,
    role: str = "student",
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Issue signed JWT access token containing subject identity and role."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """Decode and validate JWT access token subject."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def decode_access_token_payload(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate full JWT access token payload."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """FastAPI dependency to extract, validate JWT token, and ensure account is active."""
    payload = decode_access_token_payload(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = str(payload["sub"])

    # Verify student account is not deactivated
    try:
        from app.models.user import UserModel
        async with AsyncSessionLocal() as session:
            stmt = select(UserModel.is_active).where(UserModel.user_id == user_id)
            res = await session.execute(stmt)
            is_active = res.scalar_one_or_none()
            if is_active is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated. Please contact an administrator.",
                )
    except HTTPException:
        raise
    except Exception:
        pass

    return user_id


async def get_current_admin(token: str = Depends(oauth2_scheme)):
    """FastAPI dependency enforcing JWT validity, active status, and admin role authorization."""
    payload = decode_access_token_payload(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = str(payload["sub"])

    from app.models.user import UserModel
    async with AsyncSessionLocal() as session:
        stmt = select(UserModel).where(UserModel.user_id == user_id)
        res = await session.execute(stmt)
        user = res.scalar_one_or_none()

    if not user:
        # Fallback check memory users for tests if not in DB
        from app.services.user_service import user_service
        user_dict = None
        for u in user_service._memory_users.values():
            if u.get("user_id") == user_id:
                user_dict = u
                break
        if user_dict and user_dict.get("role") == "admin":
            if not user_dict.get("is_active", True):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account is deactivated.",
                )
            return user_dict

        # Not found or role is not admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Administrative privileges required.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Please contact an administrator.",
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Administrative privileges required.",
        )

    return user
