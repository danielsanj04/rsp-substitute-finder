from app.services.query_parser import parse_search_input


def test_parse_search_input_extracts_nvent_hoffman_brand_and_part_number():
    parsed = parse_search_input(product_details="nVent Hoffman CSD24168")

    assert parsed.part_number == "CSD24168"
    assert parsed.manufacturer == "nVent Hoffman"
    assert parsed.keywords == []


def test_parse_search_input_handles_brand_alias_and_keywords():
    parsed = parse_search_input(product_details="hoffman enclosure CSD24168")

    assert parsed.part_number == "CSD24168"
    assert parsed.manufacturer == "nVent Hoffman"
    assert parsed.keywords == ["enclosure"]


def test_parse_search_input_prefers_full_product_details_over_bad_first_token_part_number():
    parsed = parse_search_input(part_number="nVent", product_details="nVent Hoffman CSD24168")

    assert parsed.part_number == "CSD24168"
    assert parsed.manufacturer == "nVent Hoffman"
    assert parsed.keywords == []


def test_parse_search_input_keeps_part_number_only_queries():
    parsed = parse_search_input(product_details="CSD24168")

    assert parsed.part_number == "CSD24168"
    assert parsed.manufacturer is None
    assert parsed.keywords == []


def test_parse_search_input_extracts_all_caps_part_without_digits_from_freeform_query():
    parsed = parse_search_input(product_details="nVent Hoffman ENCJK")

    assert parsed.part_number == "ENCJK"
    assert parsed.manufacturer == "nVent Hoffman"
    assert parsed.keywords == []
