from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


class SubstituteRequest(BaseModel):
    """Search input from the browser extension popup.

    Users may know the exact part number, the manufacturer, or only rough product
    details. Require at least one searchable field so the backend never receives
    an empty lookup.
    """

    part_number: str | None = Field(default=None, min_length=1, examples=["A20H1608SSLP"])
    manufacturer: str | None = Field(default=None, min_length=1, examples=["Hoffman"])
    product_details: str | None = Field(
        default=None,
        min_length=1,
        examples=["stainless steel enclosure, 20 x 16 x 8"],
    )

    @model_validator(mode="after")
    def require_search_input(self) -> "SubstituteRequest":
        if not any(_has_value(value) for value in [self.part_number, self.manufacturer, self.product_details]):
            raise ValueError("Provide a part_number, manufacturer, or product_details.")
        return self


class SearchMetadata(BaseModel):
    submitted_part_number: str | None = None
    submitted_manufacturer: str | None = None
    submitted_product_details: str | None = None
    parsed_part_number: str | None = None
    parsed_manufacturer: str | None = None
    parsed_keywords: list[str] = Field(default_factory=list)
    query_text: str


class OriginalPart(BaseModel):
    part_number: str
    manufacturer: str | None = None
    description: str | None = None
    specifications: dict[str, str] = Field(default_factory=dict)
    source_link: HttpUrl | None = None


class SubstitutePart(BaseModel):
    part_number: str
    manufacturer: str | None = None
    description: str | None = None
    vendor: str
    match_percent: int = Field(..., ge=0, le=100)
    stock_status: str | None = None
    condition: str = "New"
    product_link: HttpUrl
    specifications: dict[str, str] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)


class ComparisonRow(BaseModel):
    specification: str
    original_value: str | None = None
    substitute_value: str | None = None
    match: bool
    status: str = Field(
        ...,
        description="Comparison result: match, different, missing_from_original, or missing_from_substitute.",
    )


class ApprovedVendorListResponse(BaseModel):
    vendors: list[str]
    count: int


class SubstituteResponse(BaseModel):
    search: SearchMetadata
    original_part: OriginalPart
    original_stock_options: list[SubstitutePart] = Field(default_factory=list)
    substitute_options: list[SubstitutePart] = Field(default_factory=list)
    substitutes: list[SubstitutePart] = Field(
        default_factory=list,
        description="Backward-compatible alias for substitute_options.",
    )
    comparison_table: list[ComparisonRow] = Field(default_factory=list)
    recommendation_status: Literal[
        "original_stock_found",
        "substitutes_found",
        "no_approved_substitute_found",
    ]
    customer_ready_response: str
    sales_email_summary: str = Field(
        ...,
        description="Backward-compatible alias for customer_ready_response.",
    )


def _has_value(value: str | None) -> bool:
    return value is not None and bool(value.strip())
