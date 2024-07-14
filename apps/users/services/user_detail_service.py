from typing import Any

from rest_framework.serializers import ValidationError

from apps.constants.error_messages import USER_HAS_NOT_USER_DETAIL
from apps.users.dto.user_detail_dto import ResponseUserDetailDTO, RequestUserDetailDTO
from apps.users.errors.user_detail_errors import UserDetailBadRequest
from apps.users.errors.user_errors import UserDataValidationError
from apps.users.models import User, UserDetail
from apps.users.repositories.user_detail_repository import UserDetailRepository
from apps.utils import content_utils
from apps.utils.content_utils import check_and_update_entity_with_new_data_helper


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
        content_utils.check_content_helper(user_detail)
        response_user_detail = ResponseUserDetailDTO(user_detail)
        return response_user_detail

    def update_user_detail_by_id(self, user: User, updated_user_detail_data: dict[str, Any]):
        user_detail: UserDetail = user.user_detail

        if not user_detail:
            raise UserDetailBadRequest(
                message=USER_HAS_NOT_USER_DETAIL,
                data={"message": USER_HAS_NOT_USER_DETAIL}
            )

        serializer = RequestUserDetailDTO(instance=user_detail, data=updated_user_detail_data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                user_detail = self.__check_and_update__user_detail(
                    user_detail=user_detail,
                    updated_data=serializer.validated_data
                )

                user_detail = self.__user_detail_repository.update_user_detail(user_detail)
                return ResponseUserDetailDTO(user_detail)

        except ValidationError as err:
            raise UserDataValidationError(err=err.args[0])

    def __check_and_update__user_detail(self, user_detail: UserDetail, updated_data: dict[str, Any]) -> UserDetail:
        user_detail = check_and_update_entity_with_new_data_helper(
            entity=user_detail,
            updated_data=updated_data
        )
        return user_detail
