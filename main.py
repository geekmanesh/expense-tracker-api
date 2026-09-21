from fastapi import FastAPI

from auth.router import router as auth_router
from expenses.router import router as expense_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(expense_router)
