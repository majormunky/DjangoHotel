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
