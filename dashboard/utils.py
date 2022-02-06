import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rooms import models as room_models
from booking import models as booking_models


def get_object_or_none(model_class, *, pk):
    try:
        obj = model_class.objects.get(pk=pk)
    except model_class.ObjectDoesNotExist:
        obj = None
    return obj


def book_room(user_id, room_data):
    # convert the string of data to an object

    # setup some variables for later
    room_key = None
    room_days = []

    # go over each room in our room list
    for room in room_data:
        # our request is only about one room
        # so we just need to grab the room key from one
        # of our schedule days
        if room_key is None:
            room_key = room["room_key"]

        # build a date for the day we want the room for
        date_obj = datetime.datetime.strptime(room["room_date"], "%m-%d-%Y").date()
        room_days.append(date_obj)

    # we now have a list of days that the person wants a room for
    # we really want the start and end dates though, so we sort our list
    # and grab the first and last items to get that
    room_days = sorted(room_days)
    start_date = room_days[0]
    end_date = room_days[-1]

    # get our user for this booking
    user_obj = get_object_or_none(get_user_model(), pk=user_id)

    if user_obj == None:
        return None

    # our room key contains the floor number and the room number
    room_parts = room_key.split(":")

    # get our floor
    try:
        floor_obj = room_models.Floor.objects.get(number=room_parts[0])
    except room_models.Floor.ObjectDoesNotExist:
        return None

    # get the room number
    room_num = room_parts[1].strip()

    # get the room
    try:
        room_obj = room_models.Room.objects.get(number=room_num, floor=floor_obj)
    except room_models.Room.ObjectDoesNotExist:
        return None

    # create a new booking
    new_booking = booking_models.Booking(
        start_date=start_date,
        end_date=end_date,
        user=user_obj,
        scheduled_room=room_obj,
        status="scheduled",
    )
    new_booking.save()

    # log that it happened
    booking_log = booking_models.BookingLog(booking=new_booking, what="Booking created")
    booking_log.save()

    return new_booking