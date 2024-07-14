from typing import Any


class AbstractBaseError(Exception):

    def __init__(self, message: str, data: Any, status_code: int):
        self.data = data
        self.status_code = status_code
        self.message = message
        super().__init__(message)
