from rest_framework import status

from apps.constants.error_messages import NO_ACTIVE_USER_FOUND, TOKEN_EXPIRED, PERMISSION_DENIED
from apps.errors.abstract_base_error import AbstractBaseError


class UserNotFoundError(AbstractBaseError):

    def __init__(self):
        self.data = {'message': NO_ACTIVE_USER_FOUND}
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(message=NO_ACTIVE_USER_FOUND, data=self.data, status_code=self.status_code)


class TokenExpiredError(AbstractBaseError):

    def __init__(self):
        self.data = {'message': TOKEN_EXPIRED}
        self.status_code = status.HTTP_403_FORBIDDEN
        super().__init__(message=TOKEN_EXPIRED, data=self.data, status_code=self.status_code)


class PermissionDeniedError(AbstractBaseError):

    def __init__(self):
        self.data = {'message': PERMISSION_DENIED}
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(message=PERMISSION_DENIED, data=self.data, status_code=self.status_code)