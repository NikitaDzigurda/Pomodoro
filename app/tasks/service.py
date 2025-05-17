from dataclasses import dataclass

from app.tasks.repository import TasksRepository, TaskCache
from app.tasks.schema import TaskCreateSchema, TaskSchema


@dataclass
class TaskService:
    task_repository: TasksRepository
    task_cache: TaskCache

    async def get_tasks(self, user_id: int) -> list[TaskSchema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
        else:
            tasks = await self.task_repository.get_tasks(user_id)
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def create_task(self, task_data: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = await self.task_repository.create_task(task_data, user_id)
        return TaskSchema(id=task_id, **task_data.model_dump())
