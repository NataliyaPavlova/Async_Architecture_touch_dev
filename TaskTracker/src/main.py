from contextlib import asynccontextmanager
import uvicorn
import json

from fastapi import FastAPI, Request, HTTPException, status, BackgroundTasks
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_auth_middleware import AuthMiddleware, FastAPIUser

from src.api import healthcheck, task
from src.core.db.repository import create_tables, close_connection
from src.core.services.auth_service import AuthService
from src.core.settings import settings
from src.core.queue.rabbit_sender import event_publisher
from src.core.queue.rabbit_consumer import event_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    # await event_publisher.connect()
    # await event_consumer.connect()
    # await event_consumer.consume_be()
    # await event_consumer.consume_stream()
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
app.include_router(task.router)

backgound_tasks = BackgroundTasks()
backgound_tasks.add_task(event_consumer.consume_be)


def verify_authorization_header(headers: Request.headers) -> tuple[list[str], FastAPIUser] | RedirectResponse:
    auth_service = AuthService()
    auth_header = headers.get('Authorization')
    if not auth_header:
        response = RedirectResponse(settings.auth_login_url)
        return response

    user = auth_service.get_user(auth_header.split()[-1])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = [user.role]
    return scopes, user


# app = FastAPI()
# app.add_middleware(AuthMiddleware, verify_header=verify_authorization_header)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8880, log_level='info')
