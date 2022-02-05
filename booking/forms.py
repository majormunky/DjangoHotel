from django import forms
from booking import models


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = [
            "user",
            "start_date",
            "end_date",
            "scheduled_room",
        ]
