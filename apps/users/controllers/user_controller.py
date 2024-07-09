from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.users.repositories.user_repository import UserRepository
from apps.users.services.user_service import UserService


class UserListCreateView(APIView):
    __USER_REPOSITORY = UserRepository()
    user_service: UserService = UserService(user_repository=__USER_REPOSITORY)

    def get(self, request: Request) -> Response:
        return Response(
            data={},
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        user_data = request.data
        self.user_service.create_user(user_data)
        return Response(
            data={},
            status=status.HTTP_201_CREATED,
        )
