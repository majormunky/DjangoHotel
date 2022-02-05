from django import forms
from booking import models


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = [
            "user",
            "start_date",
            "end_date",
            "is_active",
            "check_in_time",
            "room",
            "scheduled_room",
        ]
