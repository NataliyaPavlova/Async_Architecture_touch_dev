from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_auth_middleware import AuthMiddleware, FastAPIUser

from src.api import healthcheck, account
from src.core.db.repository import create_tables, close_connection
from src.core.services.auth_service import AuthService
from src.core.settings import settings
from src.core.queue.sender import event_publisher
from src.core.queue.consumer_auth import auth_consumer
from src.core.queue.consumer_tasktracker import tasktracker_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    await event_publisher.connect()
    await auth_consumer.connect()
    await auth_consumer.consume_be()
    await auth_consumer.consume_stream()
    await tasktracker_consumer.connect()
    await tasktracker_consumer.consume_be()
    await tasktracker_consumer.consume_stream()

    yield

    close_connection()
    await event_publisher.stop()
    await auth_consumer.stop()
    await tasktracker_consumer.stop()


app = FastAPI(
    lifespan=lifespan,
    title='Awesome Accounting Popug Service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(healthcheck.router)
app.include_router(account.router)

API_PREFIX = '/api/task/'


def verify_authorization_header(auth_header: str) -> tuple[list[str], FastAPIUser] | RedirectResponse:
    auth_service = AuthService()
    if not auth_header:
        response = RedirectResponse(settings.auth_login_url)
        return response

    user = auth_service.get_user(auth_header)
    scopes = [user.role]
    return scopes, user


app = FastAPI()
app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)
