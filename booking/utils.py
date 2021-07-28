from booking import models
from rooms import models as room_models


def check_bookings_with_date_range(start, end):
    return room_models.Room.objects.filter(booking__isnull=True)
