from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from models import Categories, Tasks
from scheme.task import TaskSchema, TaskCreateSchema


@dataclass
class TasksRepository:
    db_session: AsyncSession

    async def get_tasks(self, user_id: int):
        result = await self.db_session.execute(
            select(Tasks).where(Tasks.user_id == user_id)
        )
        return result.scalars().all()

    async def get_task(self, task_id: int) -> Tasks | None:
        result = await self.db_session.execute(
            select(Tasks).where(Tasks.id == task_id)
        )
        return result.scalar_one_or_none()

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        self.db_session.add(task_model)
        await self.db_session.commit()
        await self.db_session.refresh(task_model)
        return task_model.id

    async def delete_task(self, task_id: int) -> None:
        await self.db_session.execute(delete(Tasks).where(Tasks.id == task_id))
        await self.db_session.commit()

    async def get_task_by_category(self, category_name: str) -> list[Tasks]:
        result = await self.db_session.execute(
            select(Tasks).join(Categories).where(Categories.name == category_name)
        )
        return result.scalars().all()

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        await self.db_session.execute(
            update(Tasks).where(Tasks.id == task_id).values(name=name)
        )
        await self.db_session.commit()
        return await self.get_task(task_id)
