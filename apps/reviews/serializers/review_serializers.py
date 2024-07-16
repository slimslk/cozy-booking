from django.utils import timezone
from rest_framework import serializers

from apps.constants.error_messages import RATE_NOT_CHECKED_IN, PERMISSION_DENIED
from apps.listings.dto.apartment_dto import ResponseApartmentDTO
from apps.reservations.choices.status_choices import StatusChoices
from apps.reservations.models import Reservation
from apps.reviews.models.review_model import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'rating',
            'comment'
        ]

    def create(self, validated_data):
        reservation_id = validated_data.get('reservation_id')
        user = validated_data.get('user')
        reservation: Reservation = Reservation.objects.get(pk=reservation_id)
        validated_data['listing'] = reservation.listing
        if reservation.user_id != user.id:
            raise serializers.ValidationError({'err': PERMISSION_DENIED})
        if reservation.status != StatusChoices.CHECKED_IN.name:
            # or reservation.end_date > timezone.now().date(): uncomment for data check
            raise serializers.ValidationError({'err': RATE_NOT_CHECKED_IN})

        return Review.objects.create(**validated_data)


class ReviewResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'rating',
            'comment',
            'created_at',
        ]
