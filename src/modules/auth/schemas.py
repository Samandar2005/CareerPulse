from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRegisterRequest(BaseModel):
    """Foydalanuvchini ro'yxatdan o'tkazish request body'si."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="Parol kamida 8 ta belgidan iborat bo'lishi kerak")
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)


class UserLoginRequest(BaseModel):
    """Tizimga kirish request body'si."""

    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    """Google OAuth2 token yetkazib berish body'si."""

    token: str = Field(..., description="Google oAuth2 platformasidan olingan id_token")


class TokenResponse(BaseModel):
    """JWT Tokenlar qaytadigan response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """Access tokenni yangilash uchun request."""

    refresh_token: str

class UserResponse(BaseModel):
    """Foydalanuvchi ma'lumotlarini qaytaradigan response."""

    id: UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

