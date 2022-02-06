from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
class Booking(models.Model):
    booking_choices = (
        ("new", "New"),
        ("scheduled", "Scheduled"),
        ("checked_in", "Checked-In"),
        ("completed", "Completed"),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=booking_choices, default=booking_choices[0][0]
    )
    check_in_time = models.DateTimeField(blank=True, null=True)
    room = models.OneToOneField(
        "rooms.Room", on_delete=models.CASCADE, blank=True, null=True
    )
    scheduled_room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scheduled_booking",
    )
    created_at = models.DateTimeField(default=timezone.now)

    def check_in(self):
        if self.room:
            return {
                "result": "failed",
                "message": "Current booking already has room set",
            }

        room = self.scheduled_room

        if room.booking:
            return {"result": "failed", "message": "Room is already booked"}

        self.room = room
        self.scheduled_room = None
        self.status = "checked_in"
        self.save()

        log = BookingLog(booking=self, what="User has checked in")
        log.save()
        return {"result": "success"}


class BookingLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    when = models.DateTimeField(default=timezone.now)
    what = models.TextField()
