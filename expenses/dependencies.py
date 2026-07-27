from fastapi import Depends

from sqlalchemy.orm import Session

from core.database import get_db
from users.models import User
from auth.dependencies import get_authenticated_user
from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService


def get_expense_service(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
):
    repository = ExpenseRepository(
        db=db,
        user_id=user.id,
    )

    return ExpenseService(repository)
