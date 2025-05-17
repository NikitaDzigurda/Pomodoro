from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException

from app.tasks.schema import TaskSchema, TaskCreateSchema
from app.tasks.service import TaskService
from app.tasks.repository import TasksRepository

from app.dependency import get_task_repository, get_task_service, get_current_user
from app.users.user_profile.models import UserProfile

router = APIRouter(prefix='/task', tags=['task'])


@router.get(
    '/all',
    response_model=list[TaskSchema]
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[UserProfile, Depends(get_current_user)]
):
    return await task_service.get_tasks(user_id=current_user.id)


@router.post('/', response_model=TaskSchema)
async def create_task(
    task: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    current_user: Annotated[UserProfile, Depends(get_current_user)]
):
    return await task_service.create_task(task, current_user.id)


@router.patch(
    '/{task_id}',
    response_model=TaskSchema
)
async def update_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TasksRepository, Depends(get_task_repository)],
        current_user: Annotated[UserProfile, Depends(get_current_user)]  # Проверяем, что пользователь авторизован
):
    task = await task_repository.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own tasks")

    return await task_repository.update_task_name(task_id, name)


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
        task_id: int,
        task_repository: Annotated[TasksRepository, Depends(get_task_repository)],
        current_user: Annotated[UserProfile, Depends(get_current_user)]  # Проверяем, что пользователь авторизован
):
    task = await task_repository.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tasks")

    await task_repository.delete_task(task_id)
    return {'message': 'Task deleted successfully'}

