from __future__ import annotations

"""Extract approved vendor names from the vendor cheat sheet PDF.

This script reads the PDF used as the source of truth for approved procurement
vendors and writes a clean JSON vendor list to data/approved_vendors.json.

Usage:
    python scripts/refresh_approved_vendors.py
"""

from collections import defaultdict
import json
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "Vendor Cheat Sheet (1).pdf"
OUTPUT_PATH = ROOT / "data" / "approved_vendors.json"

IGNORE_ROWS = {"Name", "LOGINS"}


def extract_vendor_names(pdf_path: Path) -> list[str]:
    doc = fitz.open(pdf_path)
    names: list[str] = []

    for page in doc:
        words = page.get_text("words")
        left_words = [w for w in words if w[0] < 160 and w[1] > 80]
        groups: dict[int, list[tuple]] = defaultdict(list)

        for word in left_words:
            ykey = round(word[1] / 3) * 3
            groups[ykey].append(word)

        for y in sorted(groups):
            row = " ".join(w[4] for w in sorted(groups[y], key=lambda t: t[0]))
            row = row.replace(" ,", ",").replace(" .", ".").strip()
            if row and row not in IGNORE_ROWS:
                names.append(row)

    return dedupe_preserve_order(names)


def dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for value in values:
        if value not in seen:
            unique.append(value)
            seen.add(value)
    return unique


def main() -> None:
    vendors = extract_vendor_names(PDF_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(vendors, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(vendors)} approved vendors to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
