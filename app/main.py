from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.expenses.router import router as expenses_router
from app.users.router import router as users_router

app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(expenses_router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
