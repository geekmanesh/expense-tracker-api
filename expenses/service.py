from fastapi import HTTPException, status

from expenses.repository import ExpenseRepository
from expenses.models import Expense


class ExpenseService:

    def __init__(self, repository: ExpenseRepository):
        self.repository = repository

    def get_all_expenses(self):
        return self.repository.get_all()

    def get_expense(self, expense_id: int):

        expense = self.repository.get_by_id(expense_id)

        if expense is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found!"
            )

        return expense

    def create_expense(self, request):

        expense = Expense(
            description=request.description,
            amount=request.amount,
        )

        return self.repository.create(expense)

    def update_expense(self, request, expense_id):
        expense = self.get_expense(expense_id)

        expense.description = request.description
        expense.amount = request.amount

        return self.repository.update(expense)

    def delete_expense(self, expense_id):
        expense = self.get_expense(expense_id)

        self.repository.delete(expense)
