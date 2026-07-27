from typing import List

from fastapi import APIRouter, status, Path, Depends

from sqlalchemy.orm import Session

from expenses.models import Expense
from expenses.schemas import (
    ExpenseCreateSchema,
    ExpenseResponseSchema,
    ExpenseUpdateSchema,
)
from expenses.repository import ExpenseRepository
from expenses.service import ExpenseService
from expenses.dependencies import get_expense_service

router = APIRouter(tags=["Expenses"])


@router.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseSchema],
)
def retrieve_expenses_list(
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_all_expenses()


@router.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def retrieve_expense(
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expense(expense_id)


@router.post("/expenses", response_model=ExpenseResponseSchema)
def create_expense(
    request: ExpenseCreateSchema,
    service: ExpenseService = Depends(get_expense_service),
):

    return service.create_expense(request)


@router.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.update_expense(request, expense_id)


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int = Path(ge=1),
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete_expense(expense_id)
