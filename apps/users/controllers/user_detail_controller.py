from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.dto.user_detail_dto import ResponseUserDetailDTO
from apps.users.errors.abstract_base_error import AbstractBaseError
from apps.users.models import User
from apps.users.repositories.user_detail_repository import UserDetailRepository
from apps.users.services.user_detail_service import UserDetailService


class UserDetailRetrieveCreateDeleteUpdateView(APIView):
    __USER_DETAIL_REPOSITORY = UserDetailRepository()
    __user_detail_service: UserDetailService = UserDetailService(user_detail_repository=__USER_DETAIL_REPOSITORY)

    def get(self, request: Request) -> Response:
        try:
            user: User
            if user := request.user:
                user_detail_response: ResponseUserDetailDTO = self.__user_detail_service.get_user_detail_by_user_id(user.id)
                return Response(
                    data=user_detail_response.data,
                    status=status.HTTP_200_OK
                )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
