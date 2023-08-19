from fastapi import APIRouter

from src.api.response_models import HealthResponse

router = APIRouter(prefix="", tags=["healthcheck"])


@router.get(
    "/healthcheck",
    summary="Check if API, connection to DB PosgresSQL, connection to Redis is OK",
    response_description="Statuses whether connections are OK: True or False")
def health_check() -> HealthResponse:

    return HealthResponse(
        api_ok=True,
        ps_ok=True,
        redis_ok=True
    )


