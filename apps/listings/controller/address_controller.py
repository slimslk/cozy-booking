from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.errors.abstract_base_error import AbstractBaseError
from apps.listings.dto.address_dto import ResponseAddressDTO, AddressSerializer, RequestAddressDTO
from apps.listings.services.address_service import AddressService
from apps.security.authentications.authentication import CustomJWTAuthentication
from apps.security.permissions.user_permission import IsAdmin, IsLessor


class BaseAddressView(APIView):
    _address_service: AddressService = AddressService()
    authentication_classes = [CustomJWTAuthentication]


class ApartmentCRUDView(BaseAddressView):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        if self.request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            return [permission() for permission in [IsAdmin | IsLessor]]

    def get(self, request: Request, apartment_id: int) -> Response:
        try:
            address = self._address_service.get_address(apartment_id)
            return Response(
                data=address.data,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(request_body=AddressSerializer)
    def post(self, request: Request, apartment_id: int) -> Response:
        try:
            address_data = request.data
            apartment_response: ResponseAddressDTO = self._address_service.create_address(address_data,
                                                                                          apartment_id)
            return Response(
                data=apartment_response.data,
                status=status.HTTP_201_CREATED
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    def delete(self, request: Request, apartment_id: int) -> Response:
        try:
            self._address_service.delete_address(apartment_id)
            return Response(
                data={"message": "Deleted successfully"},
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )

    @swagger_auto_schema(request_body=RequestAddressDTO)
    def put(self, request: Request, apartment_id: int):
        try:
            address: ResponseAddressDTO = self._address_service.update_address(
                apartment_id=apartment_id,
                address_data=request.data
            )
            return Response(
                data=address.data,
                status=status.HTTP_200_OK
            )
        except AbstractBaseError as err:
            return Response(
                data=err.data,
                status=err.status_code
            )
