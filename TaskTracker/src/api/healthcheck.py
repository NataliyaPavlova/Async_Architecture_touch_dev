from fastapi import APIRouter

from src.api.response_models import HealthResponse

router = APIRouter(prefix="", tags=["healthcheck"])


@router.get(
    "/healthcheck",
    summary="Check if API, connection to DB is OK",
    response_description="Statuses whether connections are OK: True or False")
async def health_check() -> HealthResponse:
    return HealthResponse(
        api_ok=True,
        db_ok=True
    )


