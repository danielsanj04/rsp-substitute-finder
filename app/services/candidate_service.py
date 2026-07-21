import json
from pathlib import Path

from app.api.schemas.substitutes import SubstitutePart
from app.services.link_validation_service import is_valid_product_link
from app.services.vendor_service import is_approved_vendor

APP_ROOT = Path(__file__).resolve().parents[2]
SUBSTITUTE_CANDIDATES_PATH = APP_ROOT / "data" / "substitute_candidates.json"
ALLOWED_CONDITIONS = {"new"}
MINIMUM_MATCH_PERCENT = 70


def load_substitute_candidates() -> list[dict]:
    if not SUBSTITUTE_CANDIDATES_PATH.exists():
        return []

    with SUBSTITUTE_CANDIDATES_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    raise ValueError("substitute_candidates.json must contain a JSON list of candidates")


def find_valid_original_stock_options(original_part_number: str) -> list[SubstitutePart]:
    """Return approved same-part stock options for the exact original part."""
    return _find_valid_candidates(original_part_number, same_part=True)


def find_valid_substitute_candidates(original_part_number: str) -> list[SubstitutePart]:
    """Return approved true substitutes with a different part number."""
    return _find_valid_candidates(original_part_number, same_part=False)


def _find_valid_candidates(original_part_number: str, *, same_part: bool) -> list[SubstitutePart]:
    normalized_original_part_number = original_part_number.strip().lower()
    valid_candidates: list[SubstitutePart] = []

    for candidate in load_substitute_candidates():
        candidate_original_part_number = str(candidate.get("original_part_number", "")).strip().lower()
        if candidate_original_part_number != normalized_original_part_number:
            continue

        candidate_part_number = str(candidate.get("part_number", "")).strip().lower()
        candidate_is_same_part = candidate_part_number == normalized_original_part_number
        if candidate_is_same_part != same_part:
            continue

        if not is_approved_vendor(str(candidate.get("vendor", ""))):
            continue

        if str(candidate.get("condition", "")).strip().lower() not in ALLOWED_CONDITIONS:
            continue

        if int(candidate.get("match_percent", 0)) < MINIMUM_MATCH_PERCENT:
            continue

        if not is_valid_product_link(str(candidate.get("product_link", ""))):
            continue

        candidate_payload = {
            key: value
            for key, value in candidate.items()
            if key != "original_part_number"
        }
        valid_candidates.append(SubstitutePart(**candidate_payload))

    return sorted(
        valid_candidates,
        key=lambda candidate: (
            candidate.stock_status != "In Stock",
            -candidate.match_percent,
        ),
    )
