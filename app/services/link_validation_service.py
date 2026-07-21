from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_TIMEOUT_SECONDS = 8
_ALLOWED_SCHEMES = {"http", "https"}


def is_valid_product_link(url: str | None, *, check_live: bool = True) -> bool:
    """Return True when a candidate URL is specific enough and not dead.

    The validator intentionally rejects generic homepage links because the business
    rule requires a usable product/source link, not just a vendor homepage. Live
    checking is enabled by default for runtime filtering; tests can disable or
    monkeypatch it to stay deterministic.
    """
    if not url or not isinstance(url, str):
        return False

    parsed = urlparse(url.strip())
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        return False
    if not parsed.netloc:
        return False
    if _is_generic_homepage(parsed):
        return False

    if not check_live:
        return True

    return _url_is_live(url.strip())


def _is_generic_homepage(parsed_url) -> bool:
    path_is_root = parsed_url.path in {"", "/"}
    has_no_query = not parsed_url.query
    return path_is_root and has_no_query


def _url_is_live(url: str) -> bool:
    for method in ("HEAD", "GET"):
        try:
            request = Request(
                url,
                method=method,
                headers={"User-Agent": "Mozilla/5.0 RSP-PartMatch-AI/0.1"},
            )
            with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
                return 200 <= response.status < 400
        except HTTPError as error:
            if method == "HEAD" and error.code in {403, 405}:
                continue
            return 200 <= error.code < 400
        except (URLError, TimeoutError, ValueError):
            return False

    return False
