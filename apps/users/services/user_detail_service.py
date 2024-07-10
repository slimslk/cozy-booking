from apps.users.dto.user_detail_dto import ResponseUserDetailDTO
from apps.users.errors.common_errors import NoContentFoundError
from apps.users.models import User, UserDetail
from apps.users.repositories.user_detail_repository import UserDetailRepository


class UserDetailService:

    def __init__(self, user_detail_repository: UserDetailRepository):
        self.__user_repository: UserDetailRepository = user_detail_repository

    def add_user_detail_to_user(self, user: User, user_detail: dict):
        pass

    def get_user_detail_by_user_id(self, user_id: int) -> ResponseUserDetailDTO:
        user_detail: UserDetail = self.__user_repository.get_user_details_by_user_id(user_id=user_id)
        self.__check_content(user_detail)
        response_user_detail = ResponseUserDetailDTO(user_detail)
        return response_user_detail

    def __check_content(self, content):
        if not content:
            raise NoContentFoundError()
