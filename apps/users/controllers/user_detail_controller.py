from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.users.dto.user_detail_dto import ResponseUserDetailDTO
from apps.users.errors.abstract_base_error import AbstractBaseError
from apps.users.repositories.user_detail_repository import UserDetailRepository
from apps.users.services.user_detail_service import UserDetailService


class BaseUserDetailView(APIView):
    _user_detail_repository = UserDetailRepository()
    _user_detail_service: UserDetailService = UserDetailService(user_detail_repository=_user_detail_repository)
    authentication_classes = [JWTAuthentication]


class UserDetailRetrieveCreateDeleteUpdateView(BaseUserDetailView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        try:
            if request.user:
                user_id = request.user.id

                user_detail_response: ResponseUserDetailDTO = self._user_detail_service.get_user_detail_by_user_id(user_id)
                return Response(
                    data=user_detail_response.data,
                    status=status.HTTP_200_OK
                )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    def post(self, request: Request) -> Response:
        try:
            user_data = request.data
            user = request.user
            response_user: ResponseUserDetailDTO = self._user_detail_service.add_user_detail_to_user(user, user_data)
            return Response(
                data=response_user.data,
                status=status.HTTP_201_CREATED,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    def put(self, request: Request) -> Response:
        try:
            updated_user_detail_data = request.data
            user: ResponseUserDetailDTO = self._user_detail_service.update_user_detail_by_id(request.user, updated_user_detail_data)
            return Response(
                data=user.data,
                status=status.HTTP_200_OK,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )