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
    assert booking.status == "checked_in"


@pytest.mark.django_db
def test_booking_check_in_fails_if_occupied(normal_user, booking_list):
    existing_booking = booking_list.first()
    room = existing_booking.scheduled_room

    new_booking = models.Booking(
        user=normal_user,
        start_date=existing_booking.start_date,
        end_date=existing_booking.end_date,
        scheduled_room=room,
        status="scheduled",
    )
    new_booking.save()

    # this should work
    existing_checkin = existing_booking.check_in()

    # this should fail as the room is already booked
    result = new_booking.check_in()
    assert result["result"] == "failed"
    assert result["message"] == "Room is already booked"


@pytest.mark.django_db
def test_booking_check_in_twice_will_fail(booking_list):
    booking = booking_list.first()
    first_result = booking.check_in()
    assert first_result["result"] == "success"

    result = booking.check_in()

    assert result["result"] == "failed"
    assert result["message"] == "Current booking already has room set"


@pytest.mark.django_db
def test_booking_check_in_generates_log(booking_list):
    booking = booking_list.first()
    result = booking.check_in()

    assert result["result"] == "success"
    assert booking.bookinglog_set.all().count() == 2
    assert booking.bookinglog_set.all().last().what == "User has checked in"


@pytest.mark.django_db
def test_new_booking_generates_log(booking_list):
    booking = booking_list.first()

    assert booking.bookinglog_set.all().count() == 1
    assert booking.bookinglog_set.all().first().what == "Booking created"
