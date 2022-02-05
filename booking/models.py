from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField()
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
