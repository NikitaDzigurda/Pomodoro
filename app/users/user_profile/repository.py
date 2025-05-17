from sqlalchemy import insert, select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(**user.model_dump()).returning(UserProfile.id)
        result = await self.db_session.execute(query)
        user_id: int = result.scalar_one()
        await self.db_session.commit()
        return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> UserProfile | None:
        result = await self.db_session.execute(
            select(UserProfile).where(UserProfile.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        result = await self.db_session.execute(
            select(UserProfile).where(UserProfile.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        result = await self.db_session.execute(
            select(UserProfile).where(UserProfile.email == email)
        )
        return result.scalar_one_or_none()