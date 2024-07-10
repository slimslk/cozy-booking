from rest_framework import status

from apps.users.constants.error_messages import PASSWORD_MISMATCH
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






