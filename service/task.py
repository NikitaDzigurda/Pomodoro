from dataclasses import dataclass
from repository import TasksRepository, TaskCache
from scheme import TaskCreateSchema, TaskSchema


@dataclass
class TaskService:
    task_repository: TasksRepository
    task_cache: TaskCache

    def get_tasks(self, user_id: int) -> list[TaskSchema]:
        # Сначала проверяем кеш
        if tasks := self.task_cache.get_tasks():
            return tasks  # Если задачи есть в кеше, сразу их возвращаем
        else:
            # Если кеш пуст, берем данные из БД
            tasks = self.task_repository.get_tasks(user_id)  # Передаем user_id в репозиторий
            # Конвертируем их в схемы Pydantic
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            # Кладем их в кеш, чтобы в следующий раз не делать запрос в БД
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def create_task(self, task_data: TaskCreateSchema, user_id: int) -> TaskSchema:
        task_id = self.task_repository.create_task(task_data, user_id)
        return TaskSchema(id=task_id, **task_data.model_dump())
