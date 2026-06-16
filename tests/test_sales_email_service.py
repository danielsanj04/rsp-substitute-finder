from app.api.schemas.substitutes import OriginalPart, SubstitutePart
from app.services.sales_email_service import build_sales_email_summary


def test_build_sales_email_summary_with_substitute():
    original = OriginalPart(part_number="ENCJK", manufacturer="nVent Hoffman")
    substitute = SubstitutePart(
        part_number="ENCJK",
        manufacturer="nVent Hoffman",
        vendor="Grainger",
        match_percent=100,
        stock_status="In Stock",
        condition="New",
        product_link="https://www.grainger.com/",
    )

    summary = build_sales_email_summary(original, [substitute])

    assert "nVent Hoffman ENCJK" in summary
    assert "Grainger" in summary
    assert "100% match" in summary
    assert "In Stock" in summary


def test_build_sales_email_summary_without_substitute():
    original = OriginalPart(part_number="UNKNOWN", manufacturer="Example")

    summary = build_sales_email_summary(original, [])

    assert "do not currently have an approved substitute" in summary
