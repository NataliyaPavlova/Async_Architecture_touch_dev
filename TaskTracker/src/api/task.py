from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, HTTPException, status
from starlette.authentication import requires
from starlette.requests import Request

from src.api.response_models import TaskResponse, UserResponse
from src.api.request_models import TaskRequest
from src.core.services.task_service import TaskService
from src.core.queue.rabbit_sender import event_publisher
from src.core.queue.models import BEvent, StreamEvent



router = APIRouter(prefix="", tags=["task"])


@router.post("/",
             response_model=TaskResponse,
             response_model_exclude_none=True,
             status_code=status.HTTP_201_CREATED,
             summary='Save task info in DB',
             response_description='Data about created task'
             )
async def create_task(
        task: TaskRequest,
        background_tasks: BackgroundTasks,
        task_service: TaskService = Depends(),
) -> TaskResponse:
    task_added = task_service.create(task)
    if not task_added:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    background_tasks.add_task(event_publisher.publish_be,
                              event=BEvent(name='TaskAdded', public_id=task_added.public_id))
    background_tasks.add_task(event_publisher.publish_stream,
                              event=StreamEvent(name='TaskCreated', public_id=task_added.public_id))

    return TaskResponse(
        task_id=task_added.task_id,
        description=task_added.description,
        status=task_added.status,
        popug_public_id=task_added.popug_id,
        public_id=task_added.public_id,
    )


@router.get('/',
            response_model=list[TaskResponse],
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK,
            summary='Get tasks for popug',
            response_description='All tasks assigned to popug'
            )
async def get_popug_tasks(
        request: Request,
        task_service: TaskService = Depends()
) -> list[TaskResponse]:
    tasks = task_service.get_popug_tasks(request.user.public_id)
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks assigned to the popug",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return [
        TaskResponse(
            task_id=task.task_id,
            description=task.description,
            status=task.status,
            popug_public_id=task.popug_id,
            public_id=task.public_id,
        ) for task in tasks
    ]


@router.get("/task/internal/{task_id}", response_model=TaskResponse)
async def get_task_info(
        task_id: str,
        task_service: TaskService = Depends()
):
    # to do check secret in headers
    task = task_service.get_task(task_id)
    return TaskResponse(
            task_id=task.task_id,
            description=task.description,
            status=task.status,
            popug_public_id=task.popug_id,
            public_id=task.public_id,
    )


@router.get('/list',
            response_model=list[TaskResponse],
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK,
            summary='Get all but done tasks',
            response_description='All tasks with any status but "done"'

            )
@requires(['admin', 'manager'])
async def get_all_tasks(
        request: Request,
        task_service: TaskService = Depends()
) -> list[TaskResponse]:
    tasks = task_service.get_undone_tasks()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="All tasks are done",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return [
        TaskResponse(
            task_id=task.task_id,
            description=task.description,
            status=task.status,
            popug_public_id=task.popug_id,
            public_id=task.public_id,
        ) for task in tasks
    ]


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary='Make task done',
    response_description='Task is done'
)
async def update_task_status(
        task_id: int,
        background_tasks: BackgroundTasks,
        task_service: TaskService = Depends()
) -> TaskResponse:
    task_updated = task_service.update_status(task_id)
    if not task_updated:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    background_tasks.add_task(event_publisher.publish_be,
                              event=BEvent(name='TaskDone', public_id=task_updated.public_id))
    background_tasks.add_task(event_publisher.publish_stream,
                              event=StreamEvent(name='TaskUpdated', public_id=task_updated.public_id))

    return TaskResponse(
        task_id=task_updated.task_id,
        description=task_updated.description,
        status=task_updated.status,
        popug_public_id=task_updated.popug_id,
        public_id=task_updated.public_id,
    )


@router.post("/shuffle",
             response_model=list[TaskResponse],
             response_model_exclude_none=True,
             status_code=status.HTTP_200_OK,
             summary='Shuffle undone tasks',
             response_description='Undone tasks with new assignees'
             )
@requires(["admin", "manager"])
async def shuffle_tasks(
        request: Request,
        background_tasks: BackgroundTasks,
        task_service: TaskService = Depends()
) -> list[TaskResponse]:
    auth_header = request.headers.get('authorization')
    tasks_shuffled = task_service.shuffle(auth_header)
    if not tasks_shuffled:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    for task in tasks_shuffled:
        background_tasks.add_task(event_publisher.publish_be,
                                  event=BEvent(name='TaskAssigned', public_id=task.public_id))
        background_tasks.add_task(event_publisher.publish_stream,
                                  event=BEvent(name='TaskUpdated', public_id=task.public_id))

    return [TaskResponse(
        task_id=task_updated.task_id,
        description=task_updated.description,
        status=task_updated.status,
        popug_public_id=task_updated.popug_id,
        public_id=task_updated.public_id,
    ) for task_updated in tasks_shuffled]
