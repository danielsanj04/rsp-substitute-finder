from app.api.schemas.substitutes import ComparisonRow, OriginalPart, SubstitutePart


def build_comparison_table(
    original_part: OriginalPart,
    substitutes: list[SubstitutePart],
) -> list[ComparisonRow]:
    """Build a simple spec-by-spec comparison table.

    Current phase compares the first valid substitute against the original part.
    Later, we can expand this to return grouped comparisons per substitute.
    """
    if not substitutes:
        return []

    substitute = substitutes[0]
    comparison_rows: list[ComparisonRow] = []

    spec_names = sorted(
        set(original_part.specifications.keys()) | set(substitute.specifications.keys())
    )

    for spec_name in spec_names:
        original_value = original_part.specifications.get(spec_name)
        substitute_value = substitute.specifications.get(spec_name)
        status = _comparison_status(original_value, substitute_value)

        comparison_rows.append(
            ComparisonRow(
                specification=spec_name,
                original_value=original_value,
                substitute_value=substitute_value,
                match=status == "match",
                status=status,
            )
        )

    return comparison_rows


def _comparison_status(original_value: str | None, substitute_value: str | None) -> str:
    if original_value is None and substitute_value is None:
        return "missing_from_both"

    if original_value is None:
        return "missing_from_original"

    if substitute_value is None:
        return "missing_from_substitute"

    if original_value.strip().lower() == substitute_value.strip().lower():
        return "match"

    return "different"
