import json
import datetime
from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from rooms import models as floor_models
from booking import forms as booking_forms
from booking import models as booking_models
from dashboard import utils


def index(request):
    return render(request, "dashboard/index.html", {})


def setup(request):
    floor_list = floor_models.Floor.objects.all()
    return render(request, "dashboard/setup.html", {"floor_list": floor_list})


def bookings_list(request):
    bookings_list = booking_models.Booking.objects.all()
    return render(
        request, "dashboard/bookings-list.html", {"bookings_list": bookings_list}
    )


def create_booking(request):
    if request.method == "POST":
        form = booking_forms.BookingForm(request.POST)
        if form.is_valid():
            # figure out how many total days the person wants to stay
            # the date doesn't include the last day so we add 1 to our result
            total_days = (
                form.cleaned_data["end_date"] - form.cleaned_data["start_date"]
            ).days + 1

            params = urlencode(
                {
                    "user": form.cleaned_data["user"].id,
                    "start_date": form.cleaned_data["start_date"].strftime("%m-%d-%Y"),
                    "end_date": form.cleaned_data["end_date"].strftime("%m-%d-%Y"),
                    "total_days": total_days,
                }
            )
            base_url = reverse("dashboard-find-room")
            url = "{}?{}".format(base_url, params)
            return redirect(url)
    else:
        form = booking_forms.BookingForm()
    return render(request, "dashboard/create-booking.html", {"form": form})


def find_room_for_booking(request):
    sd_from_url = request.GET.get("start_date", None)
    ed_from_url = request.GET.get("end_date", None)
    user_id = request.GET.get("user", None)
    total_days = request.GET.get("total_days", None)

    if not all([sd_from_url, ed_from_url, user_id, total_days]):
        return redirect("dashboard-create-booking")

    today = datetime.datetime.today()
    start_date = datetime.datetime.strptime(sd_from_url, "%m-%d-%Y")

    date_list = utils.generate_date_list(start_date, 14)
    next_week = date_list[6]
    prev_week = start_date - datetime.timedelta(days=7)

    room_list = floor_models.Room.objects.all()

    # build up the room schedule
    room_schedule = {}

    for d in date_list:
        date_key = d.strftime("%m-%d-%Y")
        room_schedule[date_key] = []
        scheduled_room_list = floor_models.Room.objects.filter(
            scheduled_booking__start_date__lte=d, scheduled_booking__end_date__gte=d
        )
        if scheduled_room_list.exists():
            for s_room in scheduled_room_list:
                room_schedule[date_key].append(s_room)

    return render(
        request,
        "dashboard/find-room.html",
        {
            "room_list": room_list,
            "date_list": date_list,
            "today": today,
            "prev_week": prev_week,
            "next_week": next_week,
            "room_schedule": room_schedule,
            "user_id": user_id,
            "total_days": int(total_days),
        },
    )


def booking_detail(request, pk):
    booking_data = get_object_or_404(booking_models.Booking, pk=pk)
    booking_logs = booking_models.BookingLog.objects.filter(
        booking=booking_data
    ).order_by("-when")
    return render(
        request,
        "dashboard/booking-detail.html",
        {"booking_data": booking_data, "logs": booking_logs},
    )


def check_in_user(request, pk):
    booking_data = get_object_or_404(booking_models.Booking, pk=pk)

    if booking_data.check_in():
        messages.add_message(request, messages.SUCCESS, "User checked in!")
    else:
        messages.add_message(
            request, messages.ERROR, "There was a problem checking this user in"
        )
    return redirect("dashboard-booking-detail", pk=pk)


def ajax_book_room(request):
    # TODO: Perform more server side checking to be sure no room is scheduled twice

    # get the data from the request
    user_id = request.POST.get("user_id", None)
    room_list = request.POST.get("rooms")
    room_list = json.loads(room_list)

    new_booking = utils.book_room(user_id, room_list)

    if new_booking is None:
        return JsonResponse(
            {"result": "failed", "message": "Error: Unable to book room"}
        )

    new_url = reverse("dashboard-booking-detail", args=[new_booking.id])

    return JsonResponse({"result": "success", "redirect_url": new_url})
