from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.api import serializers
from rooms import models


class ListFloors(APIView):
    def get(self, request, format=None):
        floors = serializers.FloorSerializer(models.Floor.objects.all(), many=True)
        return Response(floors.data)
