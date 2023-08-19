from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Form, BackgroundTasks
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.core.models import Token, User
from src.core.user_service import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    new_user,
    get_workers,
    internal_get_popug
)
from src.core.queue.rabbit_sender import message_broker
from src.core.queue.models import BEvent, StreamEvent


router = APIRouter(prefix="", tags=["token"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.public_id}, expires_delta=access_token_expires
    )
    headers = {'Authorization': f'Bearer {access_token}'}

    return JSONResponse(
        content={'status': 'success'},
        headers=headers
    )


@router.post("/signup")
async def signup_for_access_token(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form()],
    role: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
):
    user = new_user(username, password, email, role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service Unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    background_tasks.add_task(message_broker.publish_be, BEvent(name='UserAdded', public_id=user.public_id))
    background_tasks.add_task(message_broker.publish_stream, StreamEvent(name='UserCreated', public_id=user.public_id))

    response = RedirectResponse(url='/token')
    return response


@router.get("/popug", response_model=User)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/popug/internal/{popug_id}", response_model=User)
def read_users_me(
    popug_id: str,
):
    # to do check secret in headers
    user = internal_get_popug(popug_id)
    return user


@router.get("/workers")
def get_workers_tt(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    if current_user.role in ['admin', 'manager']:
        return JSONResponse(
            content={'workers': get_workers()}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You do not have enough permissions",
        headers={"WWW-Authenticate": "Bearer"},
    )


