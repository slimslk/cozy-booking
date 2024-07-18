from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializers import ReviewCreateSerializer, ReviewResponseSerializer
from apps.security.authentications.authentication import CustomJWTAuthentication
from apps.security.permissions.user_permission import IsAdmin, IsLessor, IsRenter


class ReviewCreateView(CreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAdmin | IsLessor | IsRenter]

    def perform_create(self, serializer):
        try:
            user = self.request.user
            reservation_id = self.kwargs.get('pk')
            serializer.save(user=user, reservation_id=reservation_id)
        except IntegrityError as err:
            raise ValidationError({'err': err.args[1]})


class ReviewListView(ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ReviewResponseSerializer
    permission_classes = [IsAdmin]
    queryset = Review.objects.all()


class ReviewDeleteView(DestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAdmin]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(pk=pk).all()


class ReviewListForListing(ListAPIView):
    authentication_classes = [CustomJWTAuthentication]
    serializer_class = ReviewResponseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        listing_id = self.kwargs.get('pk')
        return Review.objects.filter(listing_id=listing_id).all()
