from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rooms.api import serializers
from rooms import models


class ListFloors(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        floors = serializers.FloorSerializer(models.Floor.objects.all(), many=True)
        return Response(floors.data)


class RoomsForFloorAPIView(APIView):
    def get(self, request, format=None):
        floor_num = request.GET.get("floor_num", None)
        if floor_num is None:
            return Response("no floor num")

        floor_data = models.Floor.objects.filter(number=floor_num)
        if not floor_data:
            return Response("no floor found")

        room_list = models.Room.objects.filter(floor=floor_data.first())
        json_data = serializers.RoomSerializer(room_list, many=True).data
        return Response(json_data)
