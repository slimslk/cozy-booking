from typing import Any

from rest_framework.serializers import ValidationError

from apps.users.dto.user_detail_dto import ResponseUserDetailDTO, RequestUserDetailDTO
from apps.users.errors.common_errors import NoContentFoundError
from apps.users.errors.user_errors import NoDataToUpdateError, UserDataValidationError
from apps.users.models import User, UserDetail
from apps.users.repositories.user_detail_repository import UserDetailRepository


class UserDetailService:

    def __init__(self, user_detail_repository: UserDetailRepository):
        self.__user_detail_repository: UserDetailRepository = user_detail_repository

    def add_user_detail_to_user(self, user: User, user_detail: dict[str, Any]):
        serializer: RequestUserDetailDTO = RequestUserDetailDTO(data=user_detail)
        if serializer.is_valid(raise_exception=True):
            user_data: dict[str, Any] = serializer.validated_data
            user_detail = self.__user_detail_repository.create_user_detail(user_data)
            user.user_detail = user_detail
            user.save()  # TODO Refactor this to use user service to update user info
            return ResponseUserDetailDTO(user_detail)

    def get_user_detail_by_user_id(self, user_id: int) -> ResponseUserDetailDTO:
        user_detail: UserDetail = self.__user_detail_repository.get_user_details_by_user_id(user_id=user_id)
        self.__check_content(user_detail)
        response_user_detail = ResponseUserDetailDTO(user_detail)
        return response_user_detail

    def update_user_detail_by_id(self, user: User, updated_user_detail_data: dict[str, Any]):
        user_detail: UserDetail = user.user_detail
        if not user_detail:
            user_detail = UserDetail()
        serializer = RequestUserDetailDTO(instance=user_detail, data=updated_user_detail_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                if not self.__updated_user_detail_with_new_data(user_detail=user_detail, updated_data=serializer.validated_data):
                    raise NoDataToUpdateError()

                user_detail = self.__user_detail_repository.update_user_detail(user_detail)
                return ResponseUserDetailDTO(user_detail)

        except ValidationError as err:
            raise UserDataValidationError(err=err.args[0])

    def __check_content(self, content):
        if not content:
            raise NoContentFoundError()

    def __updated_user_detail_with_new_data(self, user_detail: UserDetail, updated_data: dict[str, Any]) -> bool:
        is_updated: bool = False
        for key, value in updated_data.items():
            if getattr(user_detail, key) != value:
                setattr(user_detail, key, value)
                is_updated = True

        return is_updated

