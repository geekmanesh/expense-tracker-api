from typing import List

from fastapi import FastAPI, status, Path, HTTPException, Body
from fastapi.responses import JSONResponse

from schemas import ExpenseCreateSchema, ExpenseResponseSchema, ExpenseUpdateSchema

app = FastAPI()

expenses_list: list = [
    {"id": 1, "description": "House Rent", "amount": 125.10},
    {"id": 2, "description": "Food", "amount": 25.22},
    {"id": 3, "description": "Transport", "amount": 5.71},
]


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=List[ExpenseResponseSchema],
)
def retrieve_expenses_list():
    return expenses_list


@app.get("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def retrieve_expense(expense_id: int = Path(ge=1)):
    for expense in expenses_list:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.post("/expenses", response_model=ExpenseResponseSchema)
def create_expense(expense: ExpenseCreateSchema):
    last_expense_id = expenses_list[-1]["id"]
    id = last_expense_id + 1
    expense_data = {
        "id": id,
        "description": expense.description,
        "amount": expense.amount,
    }
    expenses_list.append(expense_data)

    return expense_data


@app.put("/expenses/{expense_id}", response_model=ExpenseResponseSchema)
def update_expense(expense: ExpenseUpdateSchema, expense_id: int = Path(ge=1)):

    for item in expenses_list:
        if item["id"] == expense_id:
            item["description"] = expense.description
            item["amount"] = expense.amount

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int = Path(ge=1)):
    for expense in expenses_list:
        if expense["id"] == expense_id:
            expenses_list.remove(expense)
            return JSONResponse(
                content="",
                status_code=status.HTTP_204_NO_CONTENT,
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )
