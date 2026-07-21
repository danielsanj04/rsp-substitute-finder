from app.api.schemas.substitutes import OriginalPart, SubstitutePart


def build_sales_email_summary(
    original_part: OriginalPart,
    substitutes: list[SubstitutePart],
    *,
    original_stock_options: list[SubstitutePart] | None = None,
) -> str:
    """Build a customer-ready stock/substitute summary.

    Current version is deterministic and safe. Later, an AI layer can polish the
    tone while keeping these facts as the source of truth.
    """
    part_label = _part_label(original_part)
    original_stock_options = original_stock_options or []

    if substitutes:
        best = substitutes[0]
        return (
            f"Hi, I researched {part_label} and found an approved substitute option: "
            f"{_part_label(best)} from {best.vendor}. This option is listed as "
            f"{best.condition} with a {best.match_percent}% match"
            f"{_stock_phrase(best)}. Please review the product link to confirm final fit before ordering."
        )

    if original_stock_options:
        best_stock = original_stock_options[0]
        return (
            f"Hi, I researched {part_label} and found the original part available from "
            f"approved vendor {best_stock.vendor}. Since this is the exact part number, "
            "it should be prioritized before considering a substitute."
        )

    return (
        f"Hi, I researched {part_label}, but I do not currently have an approved "
        "substitute recommendation available. I will continue checking approved sources "
        "and follow up if a suitable new-condition option is found."
    )


def _part_label(part: OriginalPart | SubstitutePart) -> str:
    if part.manufacturer:
        return f"{part.manufacturer} {part.part_number}"
    return part.part_number


def _stock_phrase(substitute: SubstitutePart) -> str:
    if not substitute.stock_status:
        return ""
    return f" and stock status: {substitute.stock_status}"
