from sqlalchemy.orm import Session

from expenses.models import Expense


class ExpenseRepository:
    def __init__(self, user_id: int, db: Session):
        self.db = db
        self.user_id = user_id

    def get_all(self) -> list[Expense]:
        return self.db.query(Expense).filter_by(user_id=self.user_id).all()

    def get_by_id(self, expense_id: int) -> Expense | None:
        return (
            self.db.query(Expense)
            .filter_by(user_id=self.user_id, id=expense_id)
            .one_or_none()
        )

    def create(self, expense: Expense) -> Expense:
        expense.user_id = self.user_id
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def update(self, expense: Expense) -> Expense:
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete(self, expense: Expense) -> None:
        self.db.delete(expense)
        self.db.commit()
