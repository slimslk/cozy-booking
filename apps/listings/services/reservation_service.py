from typing import Any

from django.db.models import Case, When

from apps.reservations.choices.status_choices import StatusChoices
from apps.reservations.models import Reservation
from apps.reservations.serializers.resirvation_serializers import ReservationResponseSerializer
from apps.utils import content_utils


class ReservationService:

    def get_all_reservations_related_to_lessor(self, lessor_id: int) -> list[Any]:
        preserved = Case(
            When(status=StatusChoices.PENDING, then=0),
            When(status=StatusChoices.CONFIRMED, then=1),
            When(status=StatusChoices.REJECTED, then=2),
            When(status=StatusChoices.CHECKED_IN, then=3),
        )
        reservations: list[Reservation] = (Reservation.objects
                                           .filter(listing__user_id=lessor_id)
                                           .order_by(preserved, 'start_date')
                                           .all())
        content_utils.check_content_helper(reservations)
        return [ReservationResponseSerializer(reservation).data for reservation in reservations]

    def get_all_reservations(self) -> list[Any]:
        preserved = Case(
            When(status=StatusChoices.PENDING, then=0),
            When(status=StatusChoices.CONFIRMED, then=1),
            When(status=StatusChoices.REJECTED, then=2),
            When(status=StatusChoices.CHECKED_IN, then=3),
        )
        reservations: list[Reservation] = Reservation.objects.order_by(preserved, 'start_date').all()
        content_utils.check_content_helper(reservations)
        return [ReservationResponseSerializer(reservation).data for reservation in reservations]
