from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_authenticated_user
from app.core.database import get_db
from app.expenses.repository import ExpenseRepository
from app.expenses.service import ExpenseService
from app.users.models import User


def get_expense_service(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
) -> ExpenseService:
    repository = ExpenseRepository(db=db, user_id=user.id)
    return ExpenseService(repository)
