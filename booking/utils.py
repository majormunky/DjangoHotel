from booking import models
from rooms import models as room_models


def check_bookings_with_date_range(start, end):
    """
    |------------|          => Room 1
        |------------|      => Room 2
                |------|    => Input
    """

    # first we start out with a list of all rooms
    room_list = room_models.Room.objects.all()

    # this will hold a list of rooms available
    result = []
    for room in room_list:
        # if our room doesn't have any scheduled bookings, we can add it
        if room.scheduled_booking.count() == 0:
            result.append(room)
        else:
            # this room does have some bookings in the future, loop over them
            for scheduled_booking in room.scheduled_booking.all():
                # check to see if our input range falls within the scheduled booking range
                if not (
                    end <= scheduled_booking.start_date.date()
                    or start >= scheduled_booking.end_date.date()
                ):
                    # it doesn't add it
                    result.append(room)
    return result
