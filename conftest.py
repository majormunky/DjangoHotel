import pytest
import datetime
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from rooms import models as room_models
from booking import models as booking_models


@pytest.fixture
def rooms():
    new_floor = room_models.Floor(number=1)
    new_floor.save()

    room1 = room_models.Room(number=1, floor=new_floor, bed_count=0)
    room1.save()

    room2 = room_models.Room(number=2, floor=new_floor, bed_count=0)
    room2.save()

    room3 = room_models.Room(number=3, floor=new_floor, bed_count=0)
    room3.save()

    return room_models.Room.objects.all()


@pytest.fixture
def normal_user():
    new_user = mixer.blend(get_user_model())
    new_user.save()
    return new_user


@pytest.fixture
def booking_list(normal_user, rooms):
    """
    This creates a booking situation where we have 2 rooms booked
    The 2 rooms that are booked have a staggered range of dates booked

    August 2021
    1...5....10....15....20....25....30
    |--------|                      Room 1
       |----------|                 Room 2
    """
    b1_start_date = datetime.date(2021, 8, 1)
    b1_end_date = datetime.date(2021, 8, 10)

    floor = room_models.Floor.objects.get(number=1)

    room1 = room_models.Room.objects.get(floor=floor, number=1)
    booking1 = mixer.blend(
        booking_models.Booking,
        start_date=b1_start_date,
        end_date=b1_end_date,
        scheduled_room=room1,
        user=normal_user,
    )
    booking1.save()

    b2_start_date = datetime.date(2021, 8, 4)
    b2_end_date = datetime.date(2021, 8, 15)
    room2 = room_models.Room.objects.get(floor=floor, number=2)

    booking2 = mixer.blend(
        booking_models.Booking,
        start_date=b2_start_date,
        end_date=b2_end_date,
        scheduled_room=room2,
        user=normal_user,
    )
    booking2.save()

    return booking_models.Booking.objects.all()


@pytest.fixture
def booking_list_room1_occupied(booking_list):
    room1 = room_models.Room.objects.get(number=1)

    booking1 = booking_models.Booking.objects.get(scheduled_room=room1)
    booking1.scheduled_room = None
    booking1.room = room1
    booking1.status = "checked_in"
    booking1.save()

    return booking1
