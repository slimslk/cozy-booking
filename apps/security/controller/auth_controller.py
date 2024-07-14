
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.security.errors.security_error import UserNotFoundError
from apps.security.serializers.user_auth_token_serializatior import UserObtainPairTokenSerializer
from apps.utils.cookie_utils import add_cookie


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserObtainPairTokenSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            response: Response = Response(serializer.validated_data, status=status.HTTP_200_OK)
            response = add_cookie(serializer.user, response)
            return response
        except UserNotFoundError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )


class UserLogoutView(APIView):

    def post(self, request: Request) -> Response:
        if request.user and request.user.is_authenticated:
            logout(request)

        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
