from typing import List

from fastapi import APIRouter, Depends, Path, status

from app.core.i18n import Translator, get_translator
from app.expenses.dependencies import get_expense_service
from app.expenses.schemas import (
    ExpenseCreateSchema,
    ExpenseMutationResponse,
    ExpenseResponseSchema,
    ExpenseUpdateSchema,
)
from app.expenses.service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=List[ExpenseResponseSchema])
def list_expenses(service: ExpenseService = Depends(get_expense_service)):
    return service.get_all_expenses()


@router.get("/{expense_id}", response_model=ExpenseResponseSchema)
def get_expense(
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expense(expense_id)


@router.post(
    "",
    response_model=ExpenseMutationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    request: ExpenseCreateSchema,
    service: ExpenseService = Depends(get_expense_service),
    translator: Translator = Depends(get_translator),
):
    expense = service.create_expense(request)
    return {
        "message": translator("expense_created"),
        "expense": expense,
    }


@router.put("/{expense_id}", response_model=ExpenseMutationResponse)
def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
    translator: Translator = Depends(get_translator),
):
    expense = service.update_expense(request, expense_id)
    return {
        "message": translator("expense_updated"),
        "expense": expense,
    }


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete_expense(expense_id)
