from rest_framework import status

from apps.constants.error_messages import NO_CONTENT_FOUND, NO_DATA_TO_UPDATE
from apps.errors.abstract_base_error import AbstractBaseError


class NoContentFoundError(AbstractBaseError):

    def __init__(self):
        self.status_code = status.HTTP_204_NO_CONTENT
        self.message = NO_CONTENT_FOUND
        self.data = {}
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)


class NoDataToUpdateError(AbstractBaseError):

    def __init__(self):
        self.data = {'message': NO_DATA_TO_UPDATE}
        self.status_code = status.HTTP_200_OK
        self.message = NO_DATA_TO_UPDATE
        super().__init__(message=self.message, data=self.data, status_code=self.status_code)