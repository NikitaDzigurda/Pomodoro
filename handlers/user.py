from fastapi import APIRouter, Depends
from typing import Annotated
from scheme import UserLoginSchema, UserCreateSchema
from service import UserService
from dependency import get_user_service
router = APIRouter(prefix="/user", tags=['user'])


@router.post("", response_model=UserLoginSchema)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(body.username, body.password)
