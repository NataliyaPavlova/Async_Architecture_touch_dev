from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import healthcheck, user
from src.core.db.repository import create_tables, close_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    close_connection()


app = FastAPI(
    lifespan=lifespan,
    title='Awesome Auth Popug Service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(healthcheck.router)
app.include_router(user.router)

API_PREFIX = '/api'
