import string
from dataclasses import dataclass
from scheme import UserLoginSchema
from repository import UserRepository
from random import *
from string import *


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token: str = self._generate_access_token()
        user = self.user_repository.create_user(username=username, password=password, access_token=access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))

