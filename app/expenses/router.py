from typing import List

from fastapi import APIRouter, Depends, Path, status

from app.expenses.dependencies import get_expense_service
from app.expenses.schemas import (
    ExpenseCreateSchema,
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
    response_model=ExpenseResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    request: ExpenseCreateSchema,
    service: ExpenseService = Depends(get_expense_service),
):
    return service.create_expense(request)


@router.put("/{expense_id}", response_model=ExpenseResponseSchema)
def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.update_expense(request, expense_id)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete_expense(expense_id)
