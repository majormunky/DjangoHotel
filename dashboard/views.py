from django.shortcuts import render, redirect
from rooms import models as floor_models
from booking import forms as booking_forms

# Create your views here.
def index(request):
    return render(request, "dashboard/index.html", {})


def setup(request):
    floor_list = floor_models.Floor.objects.all()
    return render(request, "dashboard/setup.html", {"floor_list": floor_list})


def bookings_list(request):
    return render(request, "dashboard/bookings-list.html", {})


def create_booking(request):
    if request.method == "POST":
        form = booking_forms.BookingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.is_active = False
            item.save()

            return redirect("dashboard-booking")
    else:
        form = booking_forms.BookingForm()
    return render(request, "dashboard/create-booking.html", {"form": form})
