class UserNotFoundedException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'User not correct password'


class InvalidTokenException(Exception):
    detail = 'Token expired'


class TokenNotCorrectException(Exception):
    detail = 'Invalid token'