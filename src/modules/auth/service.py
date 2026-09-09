from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User, UserRole
from src.modules.auth.jwt import JWTManager
from src.modules.auth.password import hash_password, verify_password
from src.modules.auth.schemas import TokenResponse, UserLoginRequest, UserRegisterRequest


class AuthService:

    @staticmethod
    async def register_user(user_data: UserRegisterRequest, session: AsyncSession) -> TokenResponse:
        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.USER,
            is_active=True,
        )

        session.add(new_user)
        try:
            await session.commit()
            await session.refresh(new_user)
        except IntegrityError as err:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ushbu email manzili bilan foydalanuvchi allaqachon ro'yxatdan o'tgan",
            ) from err

        access_token = JWTManager.create_access_token(new_user)
        refresh_token = JWTManager.create_refresh_token(new_user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @staticmethod
    async def authenticate_user(user_data: UserLoginRequest, session: AsyncSession) -> TokenResponse:
        result = await session.execute(select(User).where(User.email == user_data.email))
        user = result.scalar_one_or_none()

        # Google oAuth foydalanuvchilarida password_hash None bo'lishi mumkin
        if not user or user.password_hash is None or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email yoki parol noto'g'ri",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Foydalanuvchi hisobi bloklangan",
            )

        access_token = JWTManager.create_access_token(user)
        refresh_token = JWTManager.create_refresh_token(user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @classmethod
    async def refresh_tokens(
        cls, refresh_token: str, session: AsyncSession
    ) -> TokenResponse:
        """Refresh token orqali yangi Access va Refresh tokenlarni yaratish."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Yaroqsiz yoki muddati o'tgan refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # 1. Refresh tokenni dekod qilish
        payload = JWTManager.decode_token(refresh_token)
        if not payload or payload.get("typ") != "refresh":
            raise credentials_exception

        user_id_str: str | None = payload.get("sub")
        if not user_id_str:
            raise credentials_exception

        # 2. Foydalanuvchini bazadan qidirish va faolligini tekshirish
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise credentials_exception

        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            raise credentials_exception

        # 3. Yangi tokenlar juftligini yaratish (User ob'ektining o'zi uzatiladi)
        access_token = JWTManager.create_access_token(user)
        new_refresh_token = JWTManager.create_refresh_token(user)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )