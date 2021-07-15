from rest_framework import serializers
from rooms import models

class FloorSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()

    class Meta:
        model = models.Floor
        fields = ["id", "number", "rooms"]

    def get_rooms(self, obj):
        return obj.room_set.count()
