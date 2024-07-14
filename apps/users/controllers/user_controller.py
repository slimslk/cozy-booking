from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.security.permissions.user_permission import IsAdmin, IsRenter, IsLessor
from apps.users.dto.user_dto import ResponseUserDTO, RequestUserDTO
from apps.errors.abstract_base_error import AbstractBaseError
from apps.users.repositories.user_repository import UserRepository
from apps.users.services.user_service import UserService


class BaseUserView(APIView):
    _user_repository = UserRepository()
    _user_service: UserService = UserService(user_repository=_user_repository)
    authentication_classes = [JWTAuthentication]


class UserCRUDView(BaseUserView):
    permission_classes = [IsAdmin | IsLessor | IsRenter]

    def get_permissions(self):
        if self.request.method in ["POST"]:
            return [AllowAny()]
        if self.request.method in ["PUT", "DELETE", "GET"]:
            return [permission() for permission in [IsAdmin | IsLessor | IsRenter]]

    def get(self, request: Request):
        try:
            user: ResponseUserDTO = self._user_service.get_user_by_id(request.user.id)
            return Response(
                data=user.data,
                status=status.HTTP_201_CREATED,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(request_body=RequestUserDTO)
    def post(self, request: Request) -> Response:
        try:
            user_data = request.data
            response_user: ResponseUserDTO = self._user_service.create_user(user_data)
            return Response(
                data=response_user.data,
                status=status.HTTP_201_CREATED,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(request_body=RequestUserDTO)
    def put(self, request: Request):
        try:
            updated_user_data = request.data
            user: ResponseUserDTO = self._user_service.update_user_by_id(request.user.id, updated_user_data)
            return Response(
                data=user.data,
                status=status.HTTP_200_OK,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    def delete(self, request: Request):
        try:
            self._user_service.soft_delete_user_by_id(request.user.id)
            return Response(
                data={},
                status=status.HTTP_200_OK,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )


class UserListView(BaseUserView):
    permission_classes = [IsAdmin]

    def get(self, request: Request) -> Response:
        try:
            users: list[dict] = self._user_service.get_all_users()
            return Response(
                data=users,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
