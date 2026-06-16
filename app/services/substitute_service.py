from app.api.schemas.substitutes import SearchMetadata, SubstituteRequest, SubstituteResponse
from app.services.candidate_service import find_valid_substitute_candidates
from app.services.comparison_service import build_comparison_table
from app.services.product_research_service import research_original_part
from app.services.sales_email_service import build_sales_email_summary


def find_substitutes(request: SubstituteRequest) -> SubstituteResponse:
    """Find valid substitute recommendations for a part request.

    Current phase uses local fixture data. Later phases will replace candidate
    loading with live vendor search, scraping, stock checks, and AI-assisted
    comparison.
    """
    original_part = research_original_part(request)
    substitutes = find_valid_substitute_candidates(original_part.part_number)
    comparison_table = build_comparison_table(original_part, substitutes)
    customer_ready_response = build_sales_email_summary(original_part, substitutes)

    return SubstituteResponse(
        search=build_search_metadata(request),
        original_part=original_part,
        substitutes=substitutes,
        comparison_table=comparison_table,
        recommendation_status="matches_found" if substitutes else "no_approved_substitute_found",
        customer_ready_response=customer_ready_response,
        sales_email_summary=customer_ready_response,
    )


def build_search_metadata(request: SubstituteRequest) -> SearchMetadata:
    submitted_part_number = _clean(request.part_number)
    submitted_manufacturer = _clean(request.manufacturer)
    submitted_product_details = _clean(request.product_details)

    query_parts = [
        part
        for part in [submitted_part_number, submitted_manufacturer, submitted_product_details]
        if part
    ]

    return SearchMetadata(
        submitted_part_number=submitted_part_number,
        submitted_manufacturer=submitted_manufacturer,
        submitted_product_details=submitted_product_details,
        query_text=" | ".join(query_parts),
    )


def _clean(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None
