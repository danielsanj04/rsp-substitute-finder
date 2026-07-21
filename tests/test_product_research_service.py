from app.api.schemas.substitutes import SubstituteRequest
from app.services.product_research_service import research_original_part


def test_research_original_part_returns_structured_placeholder_for_unknown_product():
    request = SubstituteRequest(part_number=" A20H1608SSLP ", manufacturer=" Hoffman ")

    original_part = research_original_part(request)

    assert original_part.part_number == "A20H1608SSLP"
    assert original_part.manufacturer == "nVent Hoffman"
    assert original_part.specifications == {}
    assert original_part.source_link is None


def test_research_original_part_returns_encjk_fixture():
    request = SubstituteRequest(part_number=" encjk ", manufacturer=" nVent Hoffman ")

    original_part = research_original_part(request)

    assert original_part.part_number == "ENCJK"
    assert original_part.manufacturer == "nVent Hoffman"
    assert original_part.description == "Seismic Cabinet Joining Kit, Black, Steel"
    assert original_part.specifications["material"] == "Steel"
    assert str(original_part.source_link) == "https://www.nvent.com/en-us/hoffman/products/encencjk"


def test_research_original_part_accepts_product_details_without_part_number():
    request = SubstituteRequest(product_details="stainless steel enclosure 20 x 16 x 8")

    original_part = research_original_part(request)

    assert original_part.part_number == "UNKNOWN"
    assert "stainless steel enclosure" in original_part.description
