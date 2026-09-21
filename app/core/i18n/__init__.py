"""Internationalization (i18n) helpers for the expense tracker API.

Request flow:
    HTTP request
        ↓
    language detection  (query ?lang=… or Accept-Language header)
        ↓
    FastAPI Dependency Injection  (get_language → get_translator)
        ↓
    Translator  (callable wrapper around gettext)
        ↓
    compiled .mo file
        ↓
    translated response / error detail
"""

from app.core.i18n.dependencies import get_language, get_translator
from app.core.i18n.translator import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, Translator

__all__ = [
    "DEFAULT_LANGUAGE",
    "SUPPORTED_LANGUAGES",
    "Translator",
    "get_language",
    "get_translator",
]
