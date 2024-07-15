from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.reservations.models import Reservation
from apps.reservations.serializers.resirvation_serializers import (
    ReservationUpdateSerializer,
    ReservationResponseSerializer,
    ReservationCreateSerializer,
)
from apps.security.permissions.user_permission import IsAdmin, IsRenter, IsLessor
from apps.users.choices.user_choices import RoleChoices
from apps.users.models import User


class ReservationListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin | IsRenter | IsLessor]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user: User = self.request.user
        return Reservation.objects.filter(user_id=user.id).order_by('start_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ReservationResponseSerializer
        if self.request.method in ["POST"]:
            return ReservationCreateSerializer


class ReservationUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        pk: int = self.kwargs.get("pk")
        user: User = self.request.user
        if user.role == RoleChoices.ADMIN.name:
            return Reservation.objects.filter(pk=pk)
        return Reservation.objects.filter(pk=pk, user_id=user.id)

    def get_permissions(self):
        if self.request.method in ["PUT"]:
            return [permission() for permission in [IsAdmin | IsLessor]]
        elif self.request.method in ["DELETE"]:
            return [IsAdmin()]
        return [permission() for permission in [IsAdmin | IsLessor | IsRenter]]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ReservationResponseSerializer
        if self.request.method in ["PUT"]:
            return ReservationUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
