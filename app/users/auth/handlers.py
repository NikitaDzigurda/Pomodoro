from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.schema import UserCreateSchema
from app.users.auth.service import AuthService

from app.dependency import get_auth_service
from app.exception import UserNotCorrectPasswordException, UserNotFoundedException

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post(
    '/login',
    response_model=UserLoginSchema
)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):

    try:
        return await auth_service.login(body.username, body.password)

    except UserNotFoundedException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


@router.post("/token")
async def token(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    try:
        user_dict = await auth_service.login(form_data.username, form_data.password)
        return {"access_token": user_dict.access_token, "token_type": "bearer"}

    except UserNotFoundedException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )

    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


@router.get(
    '/login/google',
    response_class=RedirectResponse
)
async def get_google_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get('/api/google')
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return await auth_service.google_auth(code=code)


@router.get('/api/yandex')
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return await auth_service.yandex_auth(code=code)


@router.get('/login/yandex')
async def get_yandex_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)