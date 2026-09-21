from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.auth.jwt import decode_token
from app.core.database import get_db
from app.core.i18n import Translator, get_translator
from app.users.models import User

ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"


def _decode_or_401(
    token: Optional[str],
    expected_type: str,
    translator: Translator,
) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translator("not_authenticated"),
        )
    try:
        payload = decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translator("token_expired"),
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translator("invalid_token"),
        )

    if payload.get("type") != expected_type:
        key = (
            "access_token_required"
            if expected_type == "access"
            else "refresh_token_required"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translator(key),
        )
    return payload


def get_authenticated_user(
    request: Request,
    db: Session = Depends(get_db),
    translator: Translator = Depends(get_translator),
) -> User:
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    payload = _decode_or_401(token, expected_type="access", translator=translator)

    user_id = payload.get("user_id")
    user_obj = db.query(User).filter_by(id=user_id).one_or_none()
    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translator("user_no_longer_exists"),
        )
    return user_obj


def get_refresh_payload(
    request: Request,
    translator: Translator = Depends(get_translator),
) -> dict:
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    return _decode_or_401(token, expected_type="refresh", translator=translator)
