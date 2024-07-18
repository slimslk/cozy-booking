from datetime import datetime

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken

from apps.users.models import User


def add_cookie(user: User, response: Response) -> Response:
    refresh_token: Token = response.data['refresh']
    access_token: Token = response.data['access']

    token = AccessToken(access_token)
    access_token_expire = datetime.fromtimestamp(token['exp'])
    token = RefreshToken(refresh_token)
    refresh_token_expire = datetime.fromtimestamp(token['exp'])

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_token_expire
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_token_expire
    )

    return response


if __name__ == '__main__':
    pass
