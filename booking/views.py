import datetime
from django.shortcuts import render
from django.http import JsonResponse
from rooms import models as room_models
from . import utils


def book_room(request):
    return render(request, "booking/book-room.html", {})


def ajax_check_booking(request):
    start_date = request.POST.get("start", None)
    end_date = request.POST.get("end", None)

    if not all([start_date, end_date]):
        return JsonResponse(
            {"result": "failed", "message": "Missing start or end date"}
        )

    start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # simple but probably slow way to find an available room
    room_list = utils.check_bookings_with_date_range(start_date_obj, end_date_obj)

    print(room_list)

    return JsonResponse({"result": "success"})
