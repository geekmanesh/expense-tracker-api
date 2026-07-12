from typing import List

from fastapi import FastAPI, status, Path, HTTPException, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from schemas import ExpenseCreateSchema, ExpenseResponseSchema, ExpenseUpdateSchema
from database import Expense, get_db

app = FastAPI()


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseSchema],
)
def retrieve_expenses_list(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def retrieve_expense(expense_id: int = Path(ge=1), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if expense:
        return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.post("/expenses", response_model=ExpenseResponseSchema)
def create_expense(request: ExpenseCreateSchema, db: Session = Depends(get_db)):
    new_expense = Expense(
        description=request.description,
        amount=request.amount,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()

    if expense:
        expense.description = request.description
        expense.amount = request.amount
        db.commit()
        db.refresh(expense)
        return expense

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int = Path(ge=1), db: Session = Depends(get_db)):
    expense = db.query(Expense).filter_by(id=expense_id).one_or_none()
    if expense:
        db.delete(expense)
        db.commit()
        return JSONResponse(
            content="",
            status_code=status.HTTP_204_NO_CONTENT,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )
