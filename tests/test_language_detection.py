"""Unit tests for language tag normalization / resolution (no HTTP)."""

from app.core.i18n.dependencies import normalize_language_tag, resolve_language


def test_normalize_simple():
    assert normalize_language_tag("fa") == "fa"
    assert normalize_language_tag("EN") == "en"


def test_normalize_region():
    assert normalize_language_tag("fa-IR") == "fa"
    assert normalize_language_tag("en_US") == "en"


def test_normalize_accept_language_list():
    assert normalize_language_tag("fa-IR,en;q=0.9") == "fa"


def test_resolve_prefers_query():
    assert resolve_language(lang="fa", accept_language="en") == "fa"


def test_resolve_uses_header_when_no_query():
    assert resolve_language(lang=None, accept_language="fa") == "fa"


def test_resolve_fallback():
    assert resolve_language(lang="de", accept_language="xx") == "en"
    assert resolve_language(lang=None, accept_language=None) == "en"
