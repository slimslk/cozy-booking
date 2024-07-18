from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, SAFE_METHODS

from apps.errors.abstract_base_error import AbstractBaseError
from apps.listings.dto.apartment_dto import ResponseApartmentDTO, RequestApartmentDTO
from apps.listings.services.listing_service import ListingService
from apps.security.authentications.authentication import CustomJWTAuthentication
from apps.security.permissions.user_permission import IsAdmin, IsLessor


class BaseApartmentView(APIView):
    _listing_service: ListingService = ListingService()
    authentication_classes = [CustomJWTAuthentication]


class ApartmentListCreateView(BaseApartmentView):

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        if self.request.method in ["POST"]:
            return [permission() for permission in [IsAdmin | IsLessor]]

    def get(self, request: Request) -> Response:
        query_parameters = request.query_params
        try:
            apartments = self._listing_service.get_all_apartments(**query_parameters)
            return Response(
                data=apartments,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(
        request_body=RequestApartmentDTO,
        tags=['Listings'],
        # manual_parameters=[
        #  openapi.Parameter(
        #      'search', openapi.IN_QUERY,
        #      description="Search by name", type=openapi.TYPE_STRING
        #  ),
        #  openapi.Parameter(
        #      'ordering', openapi.IN_QUERY,
        #      description="Ordering by created_at", type=openapi.TYPE_STRING
        #  ),
        # ]
    )
    def post(self, request: Request) -> Response:
        try:
            apartment_data = request.data
            apartment_response: ResponseApartmentDTO = self._listing_service.create_apartment(apartment_data,
                                                                                              request.user.id)
            return Response(
                data=apartment_response.data,
                status=status.HTTP_201_CREATED
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )


class ApartmentRetrieveUpdateDelete(BaseApartmentView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        if self.request.method in ["PUT", "DELETE", "PATCH"]:
            return [permission() for permission in [IsAdmin | IsLessor]]

    def get(self, request: Request, apartment_id: int) -> Response:
        try:
            user_id = self.request.user.id
            apartment = self._listing_service.get_apartments_by_id(apartment_id, user_id=user_id)
            return Response(
                data=apartment.data,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    def delete(self, request: Request, apartment_id: int) -> Response:
        try:
            self._listing_service.delete_apartments_by_id(request.user, apartment_id)
            return Response(
                data={"message": "Deleted successfully"},
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(request_body=RequestApartmentDTO)
    def put(self, request: Request, apartment_id: int):
        try:
            apartment = self._listing_service.update_apartment_by_id(user=request.user,
                                                                     apartment_id=apartment_id,
                                                                     updated_data=request.data)
            return Response(
                data=apartment.data,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )


class ApartmentListByUserIdView(BaseApartmentView):
    permission_classes = [IsAdmin | IsLessor]

    def get(self, request: Request) -> Response:
        try:
            apartments = self._listing_service.get_all_apartments_by_user_id(request.user.id)
            return Response(
                data=apartments,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
