from app.services.link_validation_service import is_valid_product_link


def test_is_valid_product_link_rejects_empty_or_non_http_urls():
    assert not is_valid_product_link("")
    assert not is_valid_product_link("not-a-url")
    assert not is_valid_product_link("ftp://example.com/product")


def test_is_valid_product_link_rejects_generic_homepage_links():
    assert not is_valid_product_link("https://www.grainger.com/")
    assert not is_valid_product_link("https://www.grainger.com")


def test_is_valid_product_link_allows_specific_http_urls_without_live_check():
    assert is_valid_product_link(
        "https://www.grainger.com/search?searchQuery=ENCJK",
        check_live=False,
    )
