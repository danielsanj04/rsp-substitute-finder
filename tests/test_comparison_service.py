from app.api.schemas.substitutes import OriginalPart, SubstitutePart
from app.services.comparison_service import build_comparison_table


def test_build_comparison_table_compares_shared_different_and_missing_specs():
    original_part = OriginalPart(
        part_number="ENCJK",
        manufacturer="nVent Hoffman",
        specifications={
            "material": "Steel",
            "color": "Black",
            "bulletin_number": "DNCY",
            "finish": "Painted",
        },
    )
    substitute = SubstitutePart(
        part_number="ENCJK",
        manufacturer="nVent Hoffman",
        vendor="Grainger",
        match_percent=100,
        condition="New",
        product_link="https://www.grainger.com/",
        specifications={
            "material": "Steel",
            "color": "Black",
            "finish": "Powder Coated",
            "product_type": "Seismic Cabinet Joining Kit",
        },
    )

    comparison_table = build_comparison_table(original_part, [substitute])

    rows_by_spec = {row.specification: row for row in comparison_table}
    assert rows_by_spec["material"].match is True
    assert rows_by_spec["material"].status == "match"
    assert rows_by_spec["color"].match is True
    assert rows_by_spec["color"].status == "match"
    assert rows_by_spec["finish"].match is False
    assert rows_by_spec["finish"].status == "different"
    assert rows_by_spec["bulletin_number"].match is False
    assert rows_by_spec["bulletin_number"].status == "missing_from_substitute"
    assert rows_by_spec["product_type"].match is False
    assert rows_by_spec["product_type"].status == "missing_from_original"


def test_build_comparison_table_returns_empty_without_substitutes():
    original_part = OriginalPart(part_number="ENCJK", specifications={"material": "Steel"})

    comparison_table = build_comparison_table(original_part, [])

    assert comparison_table == []
