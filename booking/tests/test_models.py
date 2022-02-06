import pytest
import datetime
from booking import utils
from booking import models
from rooms import models as room_models


@pytest.mark.django_db
def test_booking_check_in_works(booking_list):
    booking = booking_list.first()
    result = booking.check_in()

    assert result["result"] == "success"


@pytest.mark.django_db
def test_booking_check_in_fails_if_occupied(normal_user, booking_list):
    existing_booking = booking_list.first()
    room = existing_booking.scheduled_room

    new_booking = models.Booking(
        user=normal_user,
        start_date=existing_booking.start_date,
        end_date=existing_booking.end_date,
        scheduled_room=room,
    )
    new_booking.save()

    # this should work
    existing_checkin = existing_booking.check_in()
    print("existing checkin", existing_checkin)
    print(existing_booking.room, existing_booking.status)

    # this should fail as the room is already booked
    result = new_booking.check_in()
    print("new checkin", result)
    assert result["result"] == "failed"
