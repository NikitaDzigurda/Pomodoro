from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from typing import Annotated

from app.infrastructure.database import get_db_session
from app.infrastructure.cache import get_redis_connection
from app.settings import Settings

from app.tasks.repository import TaskCache, TasksRepository
from app.tasks.service import TaskService

from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService

from app.users.auth.client import GoogleClient, YandexClient
from app.users.auth.service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_task_repository(db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> TasksRepository:
    return TasksRepository(db_session=db_session)


async def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


async def get_task_service(
        task_repository: Annotated[TasksRepository,Depends(get_task_repository)],
        task_cache: Annotated[TaskCache, Depends(get_tasks_cache_repository)]
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(db_session: Annotated[AsyncSession, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def google_client(
    async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)]
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def yandex_client(async_client: Annotated[httpx.AsyncClient, Depends(get_async_client)]) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    google_client: Annotated[GoogleClient, Depends(google_client)],
    yandex_client: Annotated[YandexClient, Depends(yandex_client)]
) -> AuthService:
    try:
        settings = Settings()
        if not settings.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is missing in settings")

        return AuthService(user_repository=user_repository,
                           settings=settings,
                           google_client=google_client,
                           yandex_client=yandex_client)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth service initialization failed: {str(e)}")


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


async def get_current_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = user_service.auth_service.decode_access_token(auth_token)
        user = await user_service.user_repository.get_user(payload["user_id"])
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user




