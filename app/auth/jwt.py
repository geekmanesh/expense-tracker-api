from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings

ALGORITHM = "HS256"


def _create_token(user_id: int, expires_in: int, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
        "type": token_type,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def generate_access_token(user_id: int, expires_in: int = 60 * 15) -> str:
    return _create_token(user_id, expires_in, "access")


def generate_refresh_token(user_id: int, expires_in: int = 60 * 60 * 24 * 7) -> str:
    return _create_token(user_id, expires_in, "refresh")


def decode_token(token: str) -> dict:
    """Raises ExpiredSignatureError or InvalidTokenError on failure."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
