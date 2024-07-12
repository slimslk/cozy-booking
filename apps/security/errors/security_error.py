from rest_framework import status

from apps.constants.error_messages import NO_ACTIVE_USER_FOUND, TOKEN_EXPIRED
from apps.users.errors.abstract_base_error import AbstractBaseError


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
