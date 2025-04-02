from dataclasses import dataclass
from datetime import datetime as dt, timezone, timedelta

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from client import GoogleClient
from scheme import UserLoginSchema, UserCreateSchema
from repository import UserRepository
from exception import UserNotFoundedException, UserNotCorrectPasswordException, InvalidTokenException, \
    TokenNotCorrectException
from models import UserProfile
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        print(user_data)

        if user := self.user_repository.get_google_user(google_token=user_data.access_token):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = self.user_repository.create_user(create_user_data )
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundedException

        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: str):
        payload = {
            "user_id": user_id,
            "expire": (dt.now(timezone.utc) + timedelta(days=7)).timestamp()
        }
        encoded_jwt = jwt.encode(
            payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
            expire_time = dt.fromtimestamp(payload["expire"], tz=timezone.utc)

            if expire_time < dt.now(timezone.utc):
                raise InvalidTokenException

            return payload

        except JWTError:
            raise TokenNotCorrectException

