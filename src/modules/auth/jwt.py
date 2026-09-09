import datetime
import jwt
from fastapi import HTTPException, status

from src.core.config import get_settings
from src.db.models.user import User


class JWTManager:

    @staticmethod
    def create_access_token(user: User) -> str:
        role_value = user.role.value if hasattr(user.role, "value") else str(user.role)
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        expire = now + datetime.timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "sub": str(user.id),
            "role": role_value,
            "exp": int(expire.timestamp()),
            "typ": "access",
        }
        try:
            return jwt.encode(payload, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Access token yaratishda xatolik yuz berdi"
            ) from exc

    @staticmethod
    def create_refresh_token(user: User) -> str:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        expire = now + datetime.timedelta(days=get_settings().REFRESH_TOKEN_EXPIRE_DAYS)

        payload = {
            "sub": str(user.id),
            "exp": int(expire.timestamp()),
            "typ": "refresh",
        }
        try:
            return jwt.encode(payload, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM)
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Refresh token yaratishda xatolik yuz berdi"
            ) from exc

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
        except jwt.ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Tokenning amal qilish muddati tugagan"
            ) from exc
        except jwt.InvalidTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Yaroqsiz yoki noto'g'ri token"
            ) from exc