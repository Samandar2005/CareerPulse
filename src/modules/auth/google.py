from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi import HTTPException, status

from src.core.config import get_settings


class GoogleAuthVerifier:
    """Google ID Tokenlarini autentifikatsiya qilish va tekshirish servisi."""

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Google ID Tokenni verification qiladi.
        """
        try:
            id_info = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                get_settings().GOOGLE_CLIENT_ID,
            )

            if id_info.get("iss") not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Yaroqsiz Google Token Issuer",
                )

            return id_info

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google ID Token yaroqsiz yoki muddati o'tgan",
            ) from exc



