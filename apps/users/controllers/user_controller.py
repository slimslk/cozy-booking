from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.users.dto.user_dto import ResponseUserDTO
from apps.users.errors.abstract_base_error import AbstractBaseError
from apps.users.repositories.user_repository import UserRepository
from apps.users.services.user_service import UserService


class UserListCreateView(APIView):
    __USER_REPOSITORY = UserRepository()
    __user_service: UserService = UserService(user_repository=__USER_REPOSITORY)

    def get(self, request: Request) -> Response:
        try:
            users: list[dict] = self.__user_service.get_all_users()
            return Response(
                data=users,
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
            response_user: ResponseUserDTO = self.__user_service.create_user(user_data)
            return Response(
                data=response_user.data,
                status=status.HTTP_201_CREATED,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )


class UserRetrieveDeleteUpdate(APIView):
    __USER_REPOSITORY = UserRepository()
    __user_service: UserService = UserService(user_repository=__USER_REPOSITORY)

    def get(self, request: Request, user_id: int):
        try:
            user: ResponseUserDTO = self.__user_service.get_user_by_id(user_id)
            return Response(
                data=user.data,
                status=status.HTTP_201_CREATED,
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
