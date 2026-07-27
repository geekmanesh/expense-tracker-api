from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from auth.dependencies import (
    ACCESS_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
    get_authenticated_user,
    get_refresh_payload,
)
from auth.jwt import generate_access_token, generate_refresh_token
from auth.schemas import LoginRequest, MessageResponse, RegisterRequest, UserPublic
from auth.service import authenticate_user, create_user
from core.database import get_db
from users.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_TOKEN_TTL = 60 * 15  # 15 minutes
REFRESH_TOKEN_TTL = 60 * 60 * 24 * 7  # 7 days

COOKIE_KWARGS = dict(
    httponly=True,
    secure=True,  # only sent over HTTPS — set False only in local http dev
    samesite="lax",  # blocks the token being sent on cross-site POSTs
    path="/",
)


def _set_auth_cookies(response: Response, user_id: int) -> None:
    access_token = generate_access_token(user_id, ACCESS_TOKEN_TTL)
    refresh_token = generate_refresh_token(user_id, REFRESH_TOKEN_TTL)

    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        max_age=ACCESS_TOKEN_TTL,
        **COOKIE_KWARGS,
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=REFRESH_TOKEN_TTL,
        path="/auth/refresh",  # scope refresh cookie to only the refresh endpoint
        httponly=True,
        secure=True,
        samesite="lax",
    )


@router.post("/login", response_model=MessageResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    _set_auth_cookies(response, user.id)
    return {"message": "Logged in successfully"}


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(db, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    return user


@router.post("/refresh", response_model=MessageResponse)
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_payload: dict = Depends(get_refresh_payload),
):
    user_id = refresh_payload["user_id"]
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
    _set_auth_cookies(response, user.id)
    return {"message": "Session renewed"}


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response):
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth/refresh")
    return {"message": "Logged out successfully"}
