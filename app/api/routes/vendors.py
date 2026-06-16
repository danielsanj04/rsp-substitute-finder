from fastapi import APIRouter

from app.api.schemas.substitutes import ApprovedVendorListResponse
from app.services.vendor_service import load_approved_vendors

router = APIRouter(prefix="/api/v1/vendors", tags=["vendors"])


@router.get("/approved", response_model=ApprovedVendorListResponse)
def list_approved_vendors() -> ApprovedVendorListResponse:
    """Return vendors approved for substitute recommendations."""
    vendors = load_approved_vendors()
    return ApprovedVendorListResponse(vendors=vendors, count=len(vendors))
