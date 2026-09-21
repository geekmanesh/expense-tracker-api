from fastapi import Depends, FastAPI

from app.auth.router import router as auth_router
from app.core.i18n import Translator, get_translator
from app.expenses.router import router as expenses_router
from app.users.router import router as users_router

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description=(
        "Expense tracker with cookie-based auth and gettext i18n. "
        "Pass `?lang=fa` or an `Accept-Language` header to localize messages."
    ),
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(expenses_router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/welcome", tags=["i18n"])
def welcome(translator: Translator = Depends(get_translator)):
    """Demo endpoint: returns a localized welcome message."""
    return {"message": translator("welcome")}
