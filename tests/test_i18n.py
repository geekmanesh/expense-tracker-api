"""Tests for language detection and translated API messages."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_welcome_defaults_to_english():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome!"


def test_welcome_lang_query_persian():
    response = client.get("/welcome", params={"lang": "fa"})
    assert response.status_code == 200
    assert response.json()["message"] == "خوش آمدید!"


def test_welcome_lang_query_english():
    response = client.get("/welcome", params={"lang": "en"})
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome!"


def test_welcome_accept_language_persian():
    response = client.get("/welcome", headers={"Accept-Language": "fa"})
    assert response.status_code == 200
    assert response.json()["message"] == "خوش آمدید!"


def test_welcome_accept_language_english():
    response = client.get("/welcome", headers={"Accept-Language": "en"})
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome!"


def test_unsupported_language_falls_back_to_english():
    response = client.get("/welcome", params={"lang": "de"})
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome!"


def test_query_param_has_priority_over_accept_language():
    response = client.get(
        "/welcome",
        params={"lang": "fa"},
        headers={"Accept-Language": "en"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "خوش آمدید!"


def test_locale_fa_ir_normalizes_to_fa():
    response = client.get("/welcome", headers={"Accept-Language": "fa-IR"})
    assert response.status_code == 200
    assert response.json()["message"] == "خوش آمدید!"


def test_locale_en_us_normalizes_to_en():
    response = client.get("/welcome", headers={"Accept-Language": "en-US,en;q=0.9"})
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome!"


def _register_and_login(email: str) -> TestClient:
    """Return a client that keeps auth cookies after register + login."""
    auth_client = TestClient(app)
    auth_client.post(
        "/auth/register",
        json={"email": email, "password": "password123"},
    )
    login = auth_client.post(
        "/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert login.status_code == 200
    return auth_client


def test_expense_not_found_translated_english():
    auth = _register_and_login("i18n-en@example.com")
    response = auth.get("/expenses/999", params={"lang": "en"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found."


def test_expense_not_found_translated_persian():
    auth = _register_and_login("i18n-fa@example.com")
    response = auth.get("/expenses/999", params={"lang": "fa"})
    assert response.status_code == 404
    assert response.json()["detail"] == "هزینه پیدا نشد."


def test_expense_created_message_translated():
    auth = _register_and_login("i18n-create@example.com")

    en = auth.post(
        "/expenses",
        params={"lang": "en"},
        json={"description": "coffee", "amount": 4.5},
    )
    assert en.status_code == 201
    assert en.json()["message"] == "Expense created successfully."
    assert en.json()["expense"]["amount"] == 4.5

    fa = auth.post(
        "/expenses",
        params={"lang": "fa"},
        json={"description": "tea", "amount": 3.0},
    )
    assert fa.status_code == 201
    assert fa.json()["message"] == "هزینه با موفقیت ایجاد شد."


def test_invalid_credentials_translated():
    client.post(
        "/auth/register",
        json={"email": "creds@example.com", "password": "password123"},
    )
    response = client.post(
        "/auth/login",
        params={"lang": "fa"},
        json={"email": "creds@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "نام کاربری یا رمز عبور اشتباه است."
