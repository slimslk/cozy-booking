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

    @swagger_auto_schema(
        operation_description='Get All Listings',
        tags=['Listings'],
        manual_parameters=[
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Search by title or description", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'price_min', openapi.IN_QUERY,
                description="Set min price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'price_max', openapi.IN_QUERY,
                description="Set max price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'location', openapi.IN_QUERY,
                description="Search by land or city", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'rooms', openapi.IN_QUERY,
                description="Search by amount of rooms", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'apartment_type', openapi.IN_QUERY,
                enum=[
                    'Hotel',
                    'House',
                    'Apartment',
                    'Flat',
                    'Hostel',
                    'Guest_house',
                ],
                required=False,
                description="Search by apartment type", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'order', openapi.IN_QUERY,
                required=False,
                enum=[
                    'price_asc',
                    'price_desc',
                    'created_at_asc',
                    'created_at_desc',
                    'views_asc',
                    'views_desc',
                    'rating_asc',
                    'rating_desc',
                    'popular_asc',
                    'popular_desc',
                ],
                description="Ordering by price, created date, amount of the views, rating, popular search criteria",
                type=openapi.TYPE_STRING
            ),
        ]
    )
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
        operation_description='Create new listing (only for user with role lesson and admin)',
        request_body=RequestApartmentDTO,
        tags=['Listings'],
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

    @swagger_auto_schema(
        tags=['Listings'],
        operation_description='Get listings by id',
    )
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

    @swagger_auto_schema(
        request_body=RequestApartmentDTO,
        tags=['Listings'],
        operation_description='Update listing by id',
    )
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

    @swagger_auto_schema(
        tags=['Listings'],
        operation_description='Delete listing by id (only the user who add this listing is allowed to delete)',
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


class ApartmentListByUserIdView(BaseApartmentView):
    permission_classes = [IsAdmin | IsLessor]

    @swagger_auto_schema(
        tags=['Listings'],
        operation_description="Get all listings added by a user"
    )
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
