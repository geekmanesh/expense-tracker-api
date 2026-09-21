from fastapi import APIRouter, Depends

from app.auth.dependencies import get_authenticated_user
from app.users.models import User
from app.users.schemas import UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_authenticated_user)):
    return user
