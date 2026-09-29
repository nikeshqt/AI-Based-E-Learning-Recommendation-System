from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.core.security import create_access_token, get_current_user_id


class LoginJSONRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str = "student"


router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_json(credentials: LoginJSONRequest):
    """JSON login endpoint."""
    user = await user_service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    role = user.get("role", "student")
    token = create_access_token(subject=user["user_id"], role=role)
    return TokenResponse(access_token=token, user_id=user["user_id"], role=role)


@router.post("/login/oauth", response_model=TokenResponse)
async def login_oauth(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 form specification compatible login endpoint."""
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    role = user.get("role", "student")
    token = create_access_token(subject=user["user_id"], role=role)
    return TokenResponse(access_token=token, user_id=user["user_id"], role=role)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    """Register new learner account."""
    try:
        new_user = await user_service.create_user(user_in)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_authenticated_user(current_user_id: str = Depends(get_current_user_id)):
    """Retrieve currently authenticated user profile."""
    profile = await user_service.get_by_id(current_user_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return profile
