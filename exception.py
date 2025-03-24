class UserNotFoundedException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'User not correct password'