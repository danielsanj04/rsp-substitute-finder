from app.api.schemas.substitutes import SearchMetadata, SubstituteRequest, SubstituteResponse
from app.services.candidate_service import (
    find_valid_original_stock_options,
    find_valid_substitute_candidates,
)
from app.services.comparison_service import build_comparison_table
from app.services.product_research_service import research_original_part
from app.services.query_parser import parse_search_input
from app.services.sales_email_service import build_sales_email_summary


def find_substitutes(request: SubstituteRequest) -> SubstituteResponse:
    """Find original stock options and valid substitute recommendations."""
    original_part = research_original_part(request)
    original_stock_options = find_valid_original_stock_options(original_part.part_number)
    substitute_options = find_valid_substitute_candidates(original_part.part_number)
    comparison_table = build_comparison_table(original_part, substitute_options)
    customer_ready_response = build_sales_email_summary(
        original_part,
        substitute_options,
        original_stock_options=original_stock_options,
    )

    return SubstituteResponse(
        search=build_search_metadata(request),
        original_part=original_part,
        original_stock_options=original_stock_options,
        substitute_options=substitute_options,
        substitutes=substitute_options,
        comparison_table=comparison_table,
        recommendation_status=_recommendation_status(original_stock_options, substitute_options),
        customer_ready_response=customer_ready_response,
        sales_email_summary=customer_ready_response,
    )


def _recommendation_status(original_stock_options: list, substitute_options: list) -> str:
    if substitute_options:
        return "substitutes_found"

    if original_stock_options:
        return "original_stock_found"

    return "no_approved_substitute_found"


def build_search_metadata(request: SubstituteRequest) -> SearchMetadata:
    submitted_part_number = _clean(request.part_number)
    submitted_manufacturer = _clean(request.manufacturer)
    submitted_product_details = _clean(request.product_details)

    query_parts = [
        part
        for part in [submitted_part_number, submitted_manufacturer, submitted_product_details]
        if part
    ]

    parsed_input = parse_search_input(
        part_number=request.part_number,
        manufacturer=request.manufacturer,
        product_details=request.product_details,
    )

    return SearchMetadata(
        submitted_part_number=submitted_part_number,
        submitted_manufacturer=submitted_manufacturer,
        submitted_product_details=submitted_product_details,
        parsed_part_number=parsed_input.part_number,
        parsed_manufacturer=parsed_input.manufacturer,
        parsed_keywords=parsed_input.keywords,
        query_text=" | ".join(query_parts),
    )


def _clean(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None
