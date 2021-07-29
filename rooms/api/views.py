from django.contrib import messages
from rest_framework.views import APIView
from django.contrib import messages
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


class GenerateRoomsForFloorAPIView(APIView):
    def post(self, request, format=None):
        floor_num = request.POST.get("floor_num")
        room_count = int(request.POST.get("room_count"))
        floor_obj = models.Floor.objects.filter(number=floor_num)
        rooms_created = 0
        if floor_obj:
            floor_obj = floor_obj.first()
            for i in range(1, room_count + 1):
                room_obj, created = models.Room.objects.get_or_create(
                    number=str(i),
                    floor=floor_obj,
                    defaults={"bed_count": 0, "size": "small"},
                )
                if created:
                    print(room_obj)
                    rooms_created += 1
                else:
                    print("found existing room", room_obj)
            messages.add_message(
                request,
                messages.INFO,
                "Created {} floors successfully".format(rooms_created),
            )
            return Response({"result": "success", "floors_created": rooms_created})
        return Response({"result": "failed", "message": "Unable to find floor object"})
