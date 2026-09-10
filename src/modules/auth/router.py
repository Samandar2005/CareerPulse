from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database
from src.db.models.user import User
from src.modules.auth.dependencies import get_current_user
from src.modules.auth.schemas import (
    TokenRefreshRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    GoogleAuthRequest,
)
from src.modules.auth.service import AuthService
from src.modules.auth.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi foydalanuvchini ro'yxatdan o'tkazish",
)
async def register(
    user_data: UserRegisterRequest,
    session: AsyncSession = Depends(get_database),
) -> TokenResponse:
    """Foydalanuvchini ro'yxatdan o'tkazadi va Access/Refresh token juftligini qaytaradi."""
    return await AuthService.register_user(user_data, session)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Tizimga kirish va token olish",
)
async def login(
    user_data: UserLoginRequest,
    session: AsyncSession = Depends(get_database),
) -> TokenResponse:
    """Email va parol orqali autentifikatsiyadan o'tish."""
    return await AuthService.authenticate_user(user_data, session)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh token orqali yangi Access va Refresh token berish",
)
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    session: AsyncSession = Depends(get_database),
) -> TokenResponse:
    return await AuthService.refresh_tokens(refresh_data.refresh_token, session)

@router.post(
    "/google",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Google ID Token orqali kirish yoki ro'yxatdan o'tish",
)
async def google_auth(
    body: GoogleAuthRequest,
    session: AsyncSession = Depends(get_database),
) -> TokenResponse:
    """
    Frontend Google Sign-In (GIS) dan olingan ID Tokenni qabul qiladi,
    uni Google serverlari orqali tekshiradi va CareerPulse Access/Refresh token beradi.
    """
    return await AuthService.authenticate_google(body.token, session)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Joriy foydalanuvchi ma'lumotlarini olish",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
