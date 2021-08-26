from django.shortcuts import reverse
from rest_framework import serializers
from rooms import models

class FloorSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = models.Floor
        fields = ["id", "number", "rooms"]

    def get_rooms(self, obj):
        return obj.room_set.count()


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = models.Room
        fields = ["id", "number", "size", "bed_count", "url"]

    def get_url(self, obj):
        return reverse("dashboard-room-detail", args=[obj.id])
