from typing import Any

from rest_framework import status

from apps.constants.error_messages import VALIDATION_ERROR, POSITIVE_NUMBER
from apps.errors.abstract_base_error import AbstractBaseError


class ListingDataValidationError(AbstractBaseError):

    def __init__(self, err: dict[str, Any]):
        self.data = err
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = VALIDATION_ERROR
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)


class PageParameterError(AbstractBaseError):

    def __init__(self):
        self.data = {'err': POSITIVE_NUMBER}
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = POSITIVE_NUMBER
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)
