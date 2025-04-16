from dataclasses import dataclass
import httpx

from scheme.auth import GoogleUserData, YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient()

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        response = await self.async_client.get(
            "https://login.yandex.ru/info?format=json",
            headers={'Authorization': f"OAuth {access_token}"}
        )
        print(response.json())
        return YandexUserData(**response.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> dict:
        response = await self.async_client.post(
            self.settings.YANDEX_TOKEN_URL,
            data={
                'code': code,
                'client_id': self.settings.YANDEX_CLIENT_ID,
                'client_secret': self.settings.YANDEX_SECRET_KEY,
                # 'redirect_uri': self.settings.YANDEX_REDIRECT_URI,
                'grant_type': 'authorization_code'
            },
            headers={
                "Content_Type": 'application/x-www-form-urlencoded',
            }
        )
        # response = requests.post(self.settings.YANDEX_TOKEN_URL, data=data)
        print(response.json())
        return response.json()['access_token']