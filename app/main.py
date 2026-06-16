from fastapi import FastAPI

from app.api.routes.substitutes import router as substitutes_router
from app.api.routes.vendors import router as vendors_router

app = FastAPI(
    title="RSP PartMatch AI",
    description="Internal API for approved substitute part recommendations.",
    version="0.2.0",
)

app.include_router(substitutes_router)
app.include_router(vendors_router)


@app.get("/")
def home() -> dict[str, str]:
    return {
        "name": "RSP PartMatch AI",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "search": "/api/v1/search",
        "approved_vendors": "/api/v1/vendors/approved",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
