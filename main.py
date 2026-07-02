from fastapi import FastAPI, status, Path, HTTPException, Body
from fastapi.responses import JSONResponse

app = FastAPI()

expenses_list: list = [
    {"id": 1, "description": "House Rent", "amount": 125.1},
    {"id": 2, "description": "Food", "amount": 25.2},
    {"id": 3, "description": "Transport", "amount": 5.7},
]


@app.get("/expenses", status_code=status.HTTP_200_OK)
def retrieve_expenses_list():
    return JSONResponse(
        content=expenses_list,
        status_code=status.HTTP_200_OK,
    )


@app.get("/expenses/{expense_id}")
def retrieve_expense(expense_id: int = Path(ge=1)):
    for expense in expenses_list:
        if expense["id"] == expense_id:
            return JSONResponse(content=expense, status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
    )


@app.post("/expenses")
def create_expense(expense=Body()):
    last_expense_id = expenses_list[-1]["id"]
    id = last_expense_id + 1
    data = {
        "id": id,
        "description": expense.get("description"),
        "amount": expense.get("amount"),
    }
    expenses_list.append(data)

    return JSONResponse(
        content=data,
        status_code=status.HTTP_201_CREATED,
    )


@app.put("/expenses/{expense_id}")
def update_expense(expense_request=Body(), expense_id: int = Path(ge=1)):

    for expense in expenses_list:
        if expense["id"] == expense_id:
            expense["description"] = expense_request.get("description")
            expense["amount"] = expense_request.get("amount")

            return JSONResponse(content=expense, status_code=status.HTTP_200_OK)

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
