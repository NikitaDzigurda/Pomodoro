from fastapi import FastAPI

from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router
from app.tasks.handlers import router as tasks_router

app = FastAPI(redoc_url=None)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(tasks_router)

