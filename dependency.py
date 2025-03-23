from fastapi import Depends
from database import get_db_session
from repository import TaskCache, TasksRepository
from cache import get_redis_connection
from service import TaskService
from typing import Annotated


def get_task_repository() -> TasksRepository:
    db_session = get_db_session()
    return TasksRepository(db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


def get_task_service(
        task_repository: Annotated[TasksRepository,Depends(get_task_repository)],
        task_cache: Annotated[TaskCache, Depends(get_tasks_cache_repository)]
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
