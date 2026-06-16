import json
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2]
APPROVED_VENDORS_PATH = APP_ROOT / "data" / "approved_vendors.json"


def load_approved_vendors() -> list[str]:
    if not APPROVED_VENDORS_PATH.exists():
        return []

    with APPROVED_VENDORS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return [str(vendor).strip() for vendor in data if str(vendor).strip()]

    raise ValueError("approved_vendors.json must contain a JSON list of vendor names")


def is_approved_vendor(vendor_name: str) -> bool:
    approved_vendors = {vendor.lower() for vendor in load_approved_vendors()}
    return vendor_name.strip().lower() in approved_vendors
