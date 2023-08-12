from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from src.api.response_models import TaskResponse
from src.api.request_models import TaskRequest
from src.core.services.task_service import TaskService

# from src.core.user_service import (
#     authenticate_user,
#     create_access_token,
#     get_current_active_user,
#     new_user)

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
        task_service: TaskService = Depends()
) -> TaskResponse:
    task_added = task_service.create(task)
    if not task_added:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TaskResponse(
        task_id=task_added.task_id,
        description=task_added.description,
        status=task_added.status,
        popug_id=task_added.popug_id
    )


@router.get('/',
            response_model=list[TaskResponse],
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK,
            summary='Get tasks for popug',
            response_description='All tasks assigned to popug'

            )
async def get_popug_tasks(
        popug_id: int,
        task_service: TaskService = Depends()
) -> list[TaskResponse]:
    tasks = task_service.get_popug_tasks(popug_id)
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
            popug_id=task.popug_id
        ) for task in tasks
    ]


@router.get('/list',
            response_model=list[TaskResponse],
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK,
            summary='Get all but done tasks',
            response_description='All tasks with any status but "done"'

            )
async def get_all_tasks(
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
            popug_id=task.popug_id
        ) for task in tasks
    ]


@router.patch("/{task_id}",
             response_model=TaskResponse,
             response_model_exclude_none=True,
             status_code=status.HTTP_200_OK,
             summary='Make task done',
             response_description='Task is done'
             )
async def update_task_status(
        task_id: int,
        task_service: TaskService = Depends()
) -> TaskResponse:
    task_updated = task_service.update_status(task_id)
    if not task_updated:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TaskResponse(
        task_id=task_updated.task_id,
        description=task_updated.description,
        status=task_updated.status,
        popug_id=task_updated.popug_id
    )


@router.post("/shuffle",
             response_model=list[TaskResponse],
             response_model_exclude_none=True,
             status_code=status.HTTP_200_OK,
             summary='Shuffle undone tasks',
             response_description='Undone tasks with new assignees'
             )
async def shuffle_tasks(
        task_service: TaskService = Depends()
) -> list[TaskResponse]:
    tasks_shuffled = task_service.shuffle()
    if not tasks_shuffled:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong happened...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return [TaskResponse(
        task_id=task_updated.task_id,
        description=task_updated.description,
        status=task_updated.status,
        popug_id=task_updated.popug_id
    ) for task_updated in tasks_shuffled]

