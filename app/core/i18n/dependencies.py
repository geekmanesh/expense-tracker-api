"""FastAPI dependencies for language detection and translation.

Priority:
  1. ``?lang=fa`` query parameter
  2. ``Accept-Language`` HTTP header
  3. Default language (English)
"""

from __future__ import annotations

from fastapi import Depends, Header, Query

from app.core.i18n.translator import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    Translator,
    get_translator_for,
)


def normalize_language_tag(raw: str | None) -> str | None:
    """Normalize a locale tag to a short language code.

    Examples:
        ``"fa"``           → ``"fa"``
        ``"fa-IR"``        → ``"fa"``
        ``"en-US,en;q=0.9"`` → ``"en"``  (first tag only)
    """
    if not raw:
        return None

    # Accept-Language may list several tags: take the first one.
    first_tag = raw.split(",")[0].strip()
    # Drop quality weight if present: "fa;q=0.8" → "fa"
    tag = first_tag.split(";")[0].strip()
    if not tag:
        return None

    # "fa-IR" / "en_US" → "fa" / "en"
    return tag.replace("_", "-").split("-", maxsplit=1)[0].lower()


def resolve_language(
    lang: str | None = None,
    accept_language: str | None = None,
) -> str:
    """Pick a supported language from query param, then header, else default."""
    for candidate in (lang, accept_language):
        normalized = normalize_language_tag(candidate)
        if normalized in SUPPORTED_LANGUAGES:
            return normalized
    return DEFAULT_LANGUAGE


def get_language(
    lang: str | None = Query(
        default=None,
        description="Preferred language code (e.g. en, fa). Overrides Accept-Language.",
    ),
    accept_language: str | None = Header(
        default=None,
        alias="Accept-Language",
    ),
) -> str:
    """FastAPI dependency: resolve the language for the current request."""
    return resolve_language(lang=lang, accept_language=accept_language)


def get_translator(language: str = Depends(get_language)) -> Translator:
    """FastAPI dependency: Translator bound to the request language."""
    return get_translator_for(language)
