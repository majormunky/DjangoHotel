import pytest
import datetime
import pytz
from mixer.backend.django import mixer
from rooms import models as room_models
from booking import models as booking_models


@pytest.fixture
def booking_list():
    """
    This creates a booking situation where we have 2 rooms booked
    and a third room that has no bookings setup
    The 2 rooms that are booked have a staggered range of dates booked

    August 2021
    1...5....10...15...20...25...30
    |--------|                      Room 1
       |----------|                 Room 2
                                    Room 3
    """
    tz = pytz.timezone("US/Pacific")
    b1_start_date = datetime.datetime(2021, 8, 1, 17, 0, 0).astimezone(tz)
    b1_end_date = datetime.datetime(2021, 8, 10, 11, 0, 0).astimezone(tz)
    room1 = mixer.blend(room_models.Room, number="1")
    room1.save()
    booking1 = mixer.blend(
        booking_models.Booking,
        start_date=b1_start_date,
        end_date=b1_end_date,
        scheduled_room=room1,
    )
    booking1.save()

    b2_start_date = datetime.datetime(2021, 8, 4, 17, 0, 0).astimezone(tz)
    b2_end_date = datetime.datetime(2021, 8, 15, 11, 0, 0).astimezone(tz)
    room2 = mixer.blend(room_models.Room, number="2")
    room2.save()
    booking2 = mixer.blend(
        booking_models.Booking,
        start_date=b2_start_date,
        end_date=b2_end_date,
        scheduled_room=room2,
    )
    booking2.save()

    room3 = mixer.blend(room_models.Room, number="3")
    room3.save()

    return booking_models.Booking.objects.all()
