from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import healthcheck, user
from src.core.db.repository import create_tables, close_connection
from src.core.queue.rabbit_sender import message_broker

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    await message_broker.connect()
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


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8888, log_level='info')