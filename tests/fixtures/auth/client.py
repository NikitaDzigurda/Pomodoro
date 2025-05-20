from faker import Factory as FakerFactory

import httpx
import pytest
from dataclasses import dataclass

from app.settings import Settings
from app.users.auth.schema import GoogleUserData, YandexUserData

faker = FakerFactory.create()

EXISTS_GOOGLE_USER_EMAIL = 'test@gmail.com'
EXISTS_GOOGLE_USER_ID = 20


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake access token {code}"


@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        return yandex_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake access token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())


@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())



def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL,
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256()
    )

def yandex_user_info_data() -> YandexUserData:
    return YandexUserData(
        id=faker.random_number(),
        login=faker.name(),
        default_email=faker.email(),
        real_name=faker.name(),
        access_token=faker.sha256()
    )