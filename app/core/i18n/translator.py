"""Translation service: load .mo files and expose a simple Translator.

Caching note
------------
`_load_translations` is wrapped with ``functools.lru_cache`` so each language's
``.mo`` file is read from disk only once (per process). Without caching, every
request would reopen and parse the binary catalog — unnecessary work when the
files never change at runtime.
"""

from __future__ import annotations

from functools import lru_cache
from gettext import GNUTranslations, NullTranslations
from pathlib import Path

# Languages we ship catalogs for. Anything else falls back to DEFAULT_LANGUAGE.
SUPPORTED_LANGUAGES = frozenset({"en", "fa"})
DEFAULT_LANGUAGE = "en"
DOMAIN = "messages"

LOCALES_DIR = Path(__file__).resolve().parent / "locales"


class Translator:
    """Thin callable wrapper around gettext translations for one language."""

    def __init__(
        self,
        language: str,
        translations: GNUTranslations | NullTranslations,
    ) -> None:
        self.language = language
        self._translations = translations

    def __call__(self, key: str) -> str:
        """Translate a message key, e.g. ``translator("expense_not_found")``."""
        return self._translations.gettext(key)

    def gettext(self, key: str) -> str:
        return self(key)


@lru_cache(maxsize=16)
def _load_translations(language: str) -> GNUTranslations | NullTranslations:
    """Load and cache the compiled catalog for ``language``.

    Returns ``NullTranslations`` (identity pass-through) if the .mo file is
    missing — useful during development before catalogs are compiled.
    """
    mo_path = LOCALES_DIR / language / "LC_MESSAGES" / f"{DOMAIN}.mo"
    if not mo_path.is_file():
        return NullTranslations()

    with mo_path.open("rb") as catalog:
        return GNUTranslations(catalog)


def get_translator_for(language: str) -> Translator:
    """Build a Translator for a supported language (or the default)."""
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    return Translator(language, _load_translations(language))
