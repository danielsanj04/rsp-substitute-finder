import json
from pathlib import Path

from app.api.schemas.substitutes import OriginalPart, SubstituteRequest
from app.services.query_parser import parse_search_input

APP_ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_PRODUCTS_PATH = APP_ROOT / "data" / "original_products.json"
UNKNOWN_PART_NUMBER = "UNKNOWN"


def load_original_products() -> list[dict]:
    if not ORIGINAL_PRODUCTS_PATH.exists():
        return []

    with ORIGINAL_PRODUCTS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    raise ValueError("original_products.json must contain a JSON list of products")


def find_original_product_fixture(part_number: str | None, manufacturer: str | None = None) -> OriginalPart | None:
    normalized_part_number = part_number.strip().lower() if part_number else None
    normalized_manufacturer = manufacturer.strip().lower() if manufacturer else None

    # Local fixtures are keyed by exact part number. If the extension only has
    # rough product details, do not guess a fixture match yet.
    if not normalized_part_number:
        return None

    for product in load_original_products():
        product_part_number = str(product.get("part_number", "")).strip().lower()
        product_manufacturer = str(product.get("manufacturer", "")).strip().lower()

        part_number_matches = (
            normalized_part_number is None
            or product_part_number == normalized_part_number
        )
        manufacturer_matches = (
            normalized_manufacturer is None
            or product_manufacturer == normalized_manufacturer
        )

        if part_number_matches and manufacturer_matches:
            return OriginalPart(**product)

    return None


def research_original_part(request: SubstituteRequest) -> OriginalPart:
    """Research the original product details.

    Phase 2B checks a local fixture catalog first. Later, this function will use
    vendor/manufacturer searches, scraping, or AI-assisted extraction to fill in
    real product specifications and source links.
    """
    parsed_input = parse_search_input(
        part_number=request.part_number,
        manufacturer=request.manufacturer,
        product_details=request.product_details,
    )
    fixture_product = find_original_product_fixture(
        part_number=parsed_input.part_number,
        manufacturer=parsed_input.manufacturer,
    )

    if fixture_product:
        return fixture_product

    return OriginalPart(
        part_number=parsed_input.part_number or UNKNOWN_PART_NUMBER,
        manufacturer=parsed_input.manufacturer,
        description=_unknown_product_description(request),
        specifications={},
        source_link=None,
    )


def _unknown_product_description(request: SubstituteRequest) -> str:
    if request.product_details and request.product_details.strip():
        return (
            "Original product research is not connected to live sources yet. "
            f"Submitted details: {request.product_details.strip()}"
        )

    return "Original product research is not connected to live sources yet."


def _clean(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None
