from dataclasses import dataclass
from repository import TasksRepository, TaskCache
from scheme import TaskSchema


@dataclass
class TaskService:
    task_repository: TasksRepository
    task_cache: TaskCache
    def get_tasks(self):
        if tasks := self.task_cache.get_tasks():
            return tasks

        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema