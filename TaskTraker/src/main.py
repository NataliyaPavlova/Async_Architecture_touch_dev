from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from TaskTraker.src.api.v1 import healthcheck

app = FastAPI(
    title='Awesome Task Exchange System',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(healthcheck.router)

API_PREFIX = '/api/v1'


