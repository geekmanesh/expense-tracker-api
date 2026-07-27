from fastapi import APIRouter, Depends

from auth.dependencies import get_authenticated_user
from schemas import BaseUserSchema
from models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def me(user: User = Depends(get_authenticated_user)):
    return {"id": user.id, "email": user.email}
