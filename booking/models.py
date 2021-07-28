from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField()
    check_in_time = models.DateTimeField()
    room = models.OneToOneField(
        "rooms.Room", on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField()
