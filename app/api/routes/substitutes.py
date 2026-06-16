from fastapi import APIRouter

from app.api.schemas.substitutes import SubstituteRequest, SubstituteResponse
from app.services.substitute_service import find_substitutes

router = APIRouter(tags=["substitutes"])


@router.post("/substitutes", response_model=SubstituteResponse)
def get_substitutes(request: SubstituteRequest) -> SubstituteResponse:
    """Backward-compatible substitute lookup endpoint."""
    return find_substitutes(request)


@router.post("/api/v1/search", response_model=SubstituteResponse)
def search_partmatch(request: SubstituteRequest) -> SubstituteResponse:
    """Browser extension search endpoint.

    This is the preferred contract for the popup UI. It accepts a part number,
    manufacturer, product details, or any useful combination of those fields.
    """
    return find_substitutes(request)
