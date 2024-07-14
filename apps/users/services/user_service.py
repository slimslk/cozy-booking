from typing import Any

from rest_framework import serializers

from apps.users.dto.user_dto import RequestUserDTO, ResponseUserDTO
from apps.users.errors.user_errors import UserDataValidationError
from apps.users.models import User
from apps.users.repositories.user_repository import UserRepository
from apps.utils import content_utils
from apps.utils.content_utils import check_and_update_entity_with_new_data_helper


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
        content_utils.check_content_helper(users)
        response_users = [ResponseUserDTO(user).data for user in users]
        return response_users

    def get_user_by_id(self, user_id: int) -> ResponseUserDTO:
        user: User = self.__user_repository.get_user_by_id(user_id)
        content_utils.check_content_helper(user)
        response_user = ResponseUserDTO(user)
        return response_user

    def update_user_by_id(self, user_id: int, updated_data: dict) -> ResponseUserDTO:
        user: User = self.__user_repository.get_user_by_id(user_id)
        serializer = RequestUserDTO(instance=user, data=updated_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):

                user = self.__check_and_update_user(
                    user=user,
                    updated_data=serializer.validated_data
                )

                user = self.__user_repository.update_user(user)
                return ResponseUserDTO(user)

        except serializers.ValidationError as err:
            raise UserDataValidationError(err=err.args[0])

    def soft_delete_user_by_id(self, user_id: int):
        updated_data = {'is_deleted': True}
        self.update_user_by_id(user_id, updated_data)

    def __check_and_update_user(self, user: User, updated_data: dict[str, Any]) -> User:
        user = check_and_update_entity_with_new_data_helper(
            entity=user,
            updated_data=updated_data
        )
        return user
