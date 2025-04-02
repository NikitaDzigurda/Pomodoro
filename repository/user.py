from sqlalchemy import insert, select
from dataclasses import dataclass
from models import UserProfile
from sqlalchemy.orm import Session
from scheme import UserCreateSchema


@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump(),
        ).returning(UserProfile.id)

        user_id: int = self.db_session.execute(query).scalar()
        self.db_session.commit()
        return self.get_user(user_id)

    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        return self.db_session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        return self.db_session.execute(query).scalar_one_or_none()

    def get_google_user(self, google_token: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.google_access_token == google_token)
        return self.db_session.execute(query).scalar_one_or_none()
