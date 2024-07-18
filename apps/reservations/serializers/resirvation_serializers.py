from django.db.models import Q
from rest_framework import serializers
from django.utils import timezone
from django.utils.timezone import timedelta

from apps.constants.error_messages import (
    START_DATE_GREATER_END_DATE,
    DATE_IS_OCCUPIED,
    DATE_IN_PAST, PENDING_STATUS,
    PERMISSION_DENIED, USER_CANCEL_STATUS, LESSOR_STATUS, CANT_BE_CANCELED,
)
from apps.listings.dto.apartment_dto import ResponseApartmentDTO
from apps.reservations.choices.status_choices import StatusChoices
from apps.reservations.models import Reservation
from apps.users.choices.user_choices import RoleChoices


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

        reservation = Reservation.objects.filter(
            (Q(start_date__lt=end_date) & Q(end_date__gt=start_date))
            & Q(listing=listing)
            & ~Q(status__in=[
                StatusChoices.CANCELED.name,
                StatusChoices.REJECTED.name,
            ])
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
        status = validated_data.get('status')

        if instance.listing.user_id != user.id and instance.user_id != user.id:
            raise serializers.ValidationError({'err': PERMISSION_DENIED})

        if user.role == RoleChoices.RENTER.name and status != StatusChoices.CANCELED.name:
            raise serializers.ValidationError({'err': USER_CANCEL_STATUS})

        if user.role == RoleChoices.LESSOR.name and status not in [
            StatusChoices.REJECTED.name,
            StatusChoices.CONFIRMED.name,
            StatusChoices.CHECKED_IN.name,
        ]:
            raise serializers.ValidationError({'err': LESSOR_STATUS})

        start_date = instance.start_date
        if timezone.now().date() > start_date - timedelta(days=2) and status == StatusChoices.CANCELED.name:
            raise serializers.ValidationError({'err': CANT_BE_CANCELED})

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
            'id',
            'start_date',
            'end_date',
            'status',
            'listing',
        ]
