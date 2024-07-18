from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.errors.abstract_base_error import AbstractBaseError
from apps.listings.services.reservation_service import ReservationService
from apps.security.authentications.authentication import CustomJWTAuthentication
from apps.security.permissions.user_permission import IsAdmin, IsLessor
from apps.users.choices.user_choices import RoleChoices


class ReservationController(APIView):
    permission_classes = [IsAdmin | IsLessor]
    authentication_classes = [CustomJWTAuthentication]

    __reservation_service = ReservationService()

    def get(self, request: Request) -> Response:

        try:
            lessor_id = self.request.user.id
            role = self.request.user.role
            reservations = {}
            if role == RoleChoices.LESSOR.name:
                reservations = self.__reservation_service.get_all_reservations_related_to_lessor(lessor_id)
            elif role == RoleChoices.ADMIN.name:
                reservations = self.__reservation_service.get_all_reservations()
            return Response(
                data=reservations,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
