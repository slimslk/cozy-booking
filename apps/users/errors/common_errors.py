from rest_framework import status

from apps.users.constants.error_messages import NO_CONTENT_FOUND
from apps.users.errors.abstract_base_error import AbstractBaseError


class NoContentFoundError(AbstractBaseError):

    def __init__(self):
        self.status_code = status.HTTP_204_NO_CONTENT
        self.message = NO_CONTENT_FOUND
        self.data = {}
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)