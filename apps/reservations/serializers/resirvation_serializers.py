from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone

from apps.constants.error_messages import (
    START_DATE_GREATER_END_DATE,
    DATE_IS_OCCUPIED,
    DATE_IN_PAST,PENDING_STATUS,
    PERMISSION_DENIED,
)
from apps.listings.dto.apartment_dto import ResponseApartmentDTO
from apps.reservations.choices.status_choices import StatusChoices
from apps.reservations.models import Reservation


class ReservationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            'listing',
            'start_date',
            'end_date'
        ]

    def create(self, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        listing = validated_data.get('listing')

        if start_date < timezone.now().date() or end_date < timezone.now().date():
            raise serializers.ValidationError({'err': DATE_IN_PAST})

        if start_date >= end_date:
            raise serializers.ValidationError({'err': START_DATE_GREATER_END_DATE})

        end_date -= timezone.timedelta(days=1)
        start_date += timezone.timedelta(days=1)
        reservation = Reservation.objects.filter(
            (Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date]))
            & Q(listing=listing)
        ).all()

        if reservation:
            raise serializers.ValidationError({'err': DATE_IS_OCCUPIED})
        return Reservation.objects.create(**validated_data)


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'status'
        ]

    def update(self, instance: Reservation, validated_data):
        user = validated_data.get('user')
        if instance.listing.user_id != user.id:
            raise serializers.ValidationError({'err': PERMISSION_DENIED})
        status = validated_data.get('status')
        if status == StatusChoices.PENDING.name:
            raise serializers.ValidationError({'err': PENDING_STATUS})
        instance.status = status
        instance.save()
        return instance


class ReservationResponseSerializer(serializers.ModelSerializer):
    listing = ResponseApartmentDTO(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'listing',
            'start_date',
            'end_date',
            'status'
        ]
