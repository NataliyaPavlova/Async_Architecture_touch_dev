from fastapi import APIRouter

from src.core.services.healthcheck_service import HealthcheckService
from src.api.v1.response_models import HealthResponse

router = APIRouter(prefix="/api/v1", tags=["healthcheck"])


@router.get(
    "/healthcheck",
    summary="Check if API, connection to DB PosgresSQL, connection to RabbitMQ is OK",
    response_description="Statuses whether connections are OK: True or False")
async def health_check() -> HealthResponse:
    health_check_service = HealthcheckService()
    is_rabbit = await health_check_service.check_queue_connect()

    return HealthResponse(
        api_ok=True,
        ps_ok=False,
        rabbit_ok=is_rabbit
    )


