from redis import Redis
from scheme.task import TaskSchema
import json


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            tasks_json = self.redis.lrange("tasks", 0, -1)
            return [TaskSchema.model_validate(json.loads(task)) for task in tasks_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [json.dumps(task.model_dump()) for task in tasks]
        with self.redis as redis:
            redis.lpush('tasks', *tasks_json)


