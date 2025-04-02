from fastapi import Depends, security, Request, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db_session
from repository import TaskCache, TasksRepository, UserRepository
from client import GoogleClient
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from typing import Annotated
from settings import Settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_task_repository(db_session: Annotated[Session, Depends(get_db_session)]) -> TasksRepository:
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


def get_user_repository(db_session: Annotated[Session, Depends(get_db_session)]) -> UserRepository:
    return UserRepository(db_session=db_session)


def google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    google_client: Annotated[GoogleClient, Depends(google_client)]
) -> AuthService:
    try:
        settings = Settings()
        if not settings.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is missing in settings")

        return AuthService(user_repository=user_repository,
                           settings=settings,
                           google_client=google_client)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auth service initialization failed: {str(e)}")


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


def get_current_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    auth_token: Annotated[oauth2_scheme, Depends(oauth2_scheme)]
):
    # if not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Invalid token format")

    token = auth_token

    try:
        user = user_service.auth_service.decode_access_token(token)
        user = user_service.user_repository.get_user(user["user_id"])
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user




