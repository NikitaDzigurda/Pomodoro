from typing import Annotated
from fastapi import APIRouter, status, Depends
from scheme.task import TaskSchema
from service import TaskService
from repository import TasksRepository

from dependency import get_task_repository, get_task_service

router = APIRouter(prefix='/task', tags=['task'])


@router.get(
    '/all',
    response_model=list[TaskSchema]
)
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()


@router.post(
    '/',
    response_model=TaskSchema
)
async def create_task(task: TaskSchema,
                      task_repository: Annotated[TasksRepository, Depends(get_task_repository)]):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.patch(
    '/{task_id}',
    response_model=TaskSchema
)
async def update_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TasksRepository, Depends(get_task_repository)]
):

    return task_repository.update_task_name(task_id, name)


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
        task_id: int,
        task_repository: Annotated[TasksRepository, Depends(get_task_repository)]
):
    task_repository.delete_task(task_id)
    return {'message': 'task deleted successfully'}
