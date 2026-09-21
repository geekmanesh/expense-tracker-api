from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_authenticated_user
from app.core.database import get_db
from app.core.i18n import Translator, get_translator
from app.expenses.repository import ExpenseRepository
from app.expenses.service import ExpenseService
from app.users.models import User


def get_expense_service(
    db: Session = Depends(get_db),
    user: User = Depends(get_authenticated_user),
    translator: Translator = Depends(get_translator),
) -> ExpenseService:
    repository = ExpenseRepository(db=db, user_id=user.id)
    return ExpenseService(repository=repository, translator=translator)
