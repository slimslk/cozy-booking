from typing import Any

from rest_framework import status

from apps.constants.error_messages import VALIDATION_ERROR, PASSWORD_MISMATCH, NO_DATA_TO_UPDATE
from apps.users.errors.abstract_base_error import AbstractBaseError


class MismatchedPasswords(AbstractBaseError):

    def __init__(self):
        self.data = {'message': PASSWORD_MISMATCH}
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(message=PASSWORD_MISMATCH, data=self.data, status_code=self.status_code)


class IncorrectPasswordError(AbstractBaseError):

    def __init__(self, message: str):
        self.data = {'message': message}
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)


class UserDataValidationError(AbstractBaseError):

    def __init__(self, err: dict[str, Any]):
        self.data = err
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = VALIDATION_ERROR
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)


class NoDataToUpdateError(AbstractBaseError):

    def __init__(self):
        self.data = {'message': NO_DATA_TO_UPDATE}
        self.status_code = status.HTTP_200_OK
        self.message = NO_DATA_TO_UPDATE
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)






