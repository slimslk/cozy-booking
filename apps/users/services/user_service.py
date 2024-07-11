from typing import Any

from rest_framework import serializers

from apps.users.dto.user_dto import RequestUserDTO, ResponseUserDTO
from apps.users.errors.common_errors import NoContentFoundError
from apps.users.errors.user_errors import UserDataValidationError, NoDataToUpdateError
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository: UserRepository = user_repository

    def create_user(self, user_data: dict) -> ResponseUserDTO:
        serializer: RequestUserDTO = RequestUserDTO(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user_data: dict = serializer.validated_data
            user_data.pop('re_password')
            user = self.__user_repository.create_user(user_data)
            return ResponseUserDTO(user)

    def get_all_users(self) -> list[dict]:
        users: list[User] = self.__user_repository.get_all_users()
        self.__check_content(users)
        response_users = [ResponseUserDTO(user).data for user in users]
        return response_users

    def get_user_by_id(self, user_id: int) -> ResponseUserDTO:
        user: User = self.__user_repository.get_user_by_id(user_id)
        self.__check_content(user)
        response_user = ResponseUserDTO(user)
        return response_user

    def update_user_by_id(self, user_id: int, updated_data: dict) -> ResponseUserDTO:
        user: User = self.__user_repository.get_user_by_id(user_id)
        serializer = RequestUserDTO(instance=user, data=updated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):

                if not self.__updated_user_with_new_data(user=user, updated_data=serializer.validated_data):
                    raise NoDataToUpdateError()

                user = self.__user_repository.update_user(user)
                return ResponseUserDTO(user)

        except serializers.ValidationError as err:
            raise UserDataValidationError(err=err.args[0])

    def soft_delete_user_by_id(self, user_id: int):
        updated_data = {'is_deleted': True}
        self.update_user_by_id(user_id, updated_data)

    def __check_content(self, content):
        if not content:
            raise NoContentFoundError()

    def __updated_user_with_new_data(self, user: User, updated_data: dict[str, Any]) -> bool:
        is_updated: bool = False
        for key, value in updated_data.items():
            if getattr(user, key) != value:
                setattr(user, key, value)
                is_updated = True

        return is_updated
