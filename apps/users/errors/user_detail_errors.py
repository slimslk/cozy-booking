from rest_framework import status

from apps.errors.abstract_base_error import AbstractBaseError


class UserDetailBadRequest(AbstractBaseError):

    def __init__(self, data: dict[str, str], message: str):
        self.data = data
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)
