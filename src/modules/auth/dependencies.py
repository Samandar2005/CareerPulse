from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database
from src.db.models.user import User, UserRole
from src.modules.auth.jwt import JWTManager

# HTTPBearer obyektini yaratamiz
http_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_database),
) -> User:
    """JWT Access Tokenni dekodlash va joriy foydalanuvchini DB dan olish."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentifikatsiyadan o'tib bo'lmadi yoki token yaroqsiz",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # HTTPAuthorizationCredentials ob'ektidan asl tokenni ajratib olamiz
    token = credentials.credentials

    payload = JWTManager.decode_token(token)
    if not payload:
        raise credentials_exception
    
    # Token turini tekshirish (Access token emas, refresh token kelib qolishini oldini olish)
    if payload.get("typ") != "access":
        raise credentials_exception

    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise credentials_exception

    try:
        user_id = UUID(user_id_str)
    except ValueError as exc:
        raise credentials_exception from exc

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Foydalanuvchi hisobi faol emas",
        )

    return user


def require_role(required_role: UserRole):
    """Foydalanuvchi rolini tekshirish uchun Factory dependency generator."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ushbu resursga kirish uchun ruxsatingiz yetarli emas",
            )
        return current_user

    return role_checker


get_current_admin_user = require_role(UserRole.ADMIN)