import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParsedSearchInput:
    part_number: str | None = None
    manufacturer: str | None = None
    keywords: list[str] = field(default_factory=list)
    query_text: str = ""


MANUFACTURER_ALIASES: tuple[tuple[str, str], ...] = (
    ("nvent hoffman", "nVent Hoffman"),
    ("nvent-hoffman", "nVent Hoffman"),
    ("hoffman", "nVent Hoffman"),
)

PART_NUMBER_PATTERN = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9][A-Za-z0-9._/-]*$")
ALL_CAPS_PART_NUMBER_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9._/-]{3,}$")
EXPLICIT_PART_NUMBER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


def parse_search_input(
    *,
    part_number: str | None = None,
    manufacturer: str | None = None,
    product_details: str | None = None,
) -> ParsedSearchInput:
    """Normalize a messy user search into brand, part number, and keywords.

    The extension currently sends the first typed word as part_number, which can
    be wrong for searches like "nVent Hoffman CSD24168". Product details are the
    fuller source of truth when present.
    """
    submitted_part_number = _clean(part_number)
    submitted_manufacturer = _clean(manufacturer)
    submitted_details = _clean(product_details)
    source_text = submitted_details or " ".join(
        value for value in [submitted_manufacturer, submitted_part_number] if value
    )

    detected_manufacturer = submitted_manufacturer
    working_text = source_text
    if source_text:
        detected_manufacturer, working_text = _extract_manufacturer(source_text, submitted_manufacturer)

    tokens = _tokenize(working_text)
    detected_part_number = _pick_part_number(tokens) or _trusted_part_number(submitted_part_number)
    keywords = [
        token
        for token in tokens
        if token != detected_part_number and not _looks_like_manufacturer_fragment(token)
    ]

    return ParsedSearchInput(
        part_number=detected_part_number,
        manufacturer=detected_manufacturer,
        keywords=keywords,
        query_text=source_text or "",
    )


def _extract_manufacturer(source_text: str, fallback: str | None) -> tuple[str | None, str]:
    normalized = source_text.lower()
    for alias, canonical_name in MANUFACTURER_ALIASES:
        alias_pattern = re.compile(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", re.IGNORECASE)
        if alias_pattern.search(normalized):
            return canonical_name, alias_pattern.sub(" ", source_text).strip()

    return fallback, source_text


def _pick_part_number(tokens: list[str]) -> str | None:
    part_like_tokens = [
        token
        for token in tokens
        if PART_NUMBER_PATTERN.match(token) or ALL_CAPS_PART_NUMBER_PATTERN.match(token)
    ]
    if not part_like_tokens:
        return None

    return max(part_like_tokens, key=lambda token: (sum(char.isdigit() for char in token), len(token)))


def _trusted_part_number(part_number: str | None) -> str | None:
    if not part_number or not EXPLICIT_PART_NUMBER_PATTERN.match(part_number):
        return None

    return part_number.upper()


def _tokenize(value: str | None) -> list[str]:
    if not value:
        return []

    return [token.strip(",;:()[]{}") for token in value.split() if token.strip(",;:()[]{}")]


def _looks_like_manufacturer_fragment(token: str) -> bool:
    return token.lower() in {"nvent", "hoffman"}


def _clean(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None
