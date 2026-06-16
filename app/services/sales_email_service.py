from app.api.schemas.substitutes import OriginalPart, SubstitutePart


def build_sales_email_summary(
    original_part: OriginalPart,
    substitutes: list[SubstitutePart],
) -> str:
    """Build a customer-ready substitute summary.

    Current version is deterministic and safe. Later, an AI layer can polish the
    tone while keeping these facts as the source of truth.
    """
    part_label = _part_label(original_part)

    if not substitutes:
        return (
            f"Hi, I researched {part_label}, but I do not currently have an approved "
            "substitute recommendation available. I will continue checking approved sources "
            "and follow up if a suitable new-condition option is found."
        )

    best = substitutes[0]
    return (
        f"Hi, I researched {part_label} and found an approved option: "
        f"{_part_label(best)} from {best.vendor}. This option is listed as "
        f"{best.condition} with a {best.match_percent}% match"
        f"{_stock_phrase(best)}. Please review the product link to confirm final fit before ordering."
    )


def _part_label(part: OriginalPart | SubstitutePart) -> str:
    if part.manufacturer:
        return f"{part.manufacturer} {part.part_number}"
    return part.part_number


def _stock_phrase(substitute: SubstitutePart) -> str:
    if not substitute.stock_status:
        return ""
    return f" and stock status: {substitute.stock_status}"
