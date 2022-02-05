from django.shortcuts import render, reverse
from django.http import JsonResponse
from . import models
from .api import serializers
from core import utils as core_utils


def index(request):
    return render(request, "rooms/index.html", {})


def setup(request):
    floor_list = models.Floor.objects.all().order_by("number")
    return render(request, "rooms/setup.html", {"floor_list": floor_list})


# Ajax views


def ajax_create_floor(request):
    if not request.is_ajax():
        return JsonResponse({"result": "failed", "message": "Invalid Request"})
    floor_num = request.POST.get("floor-number", None)
    if floor_num is None:
        return JsonResponse({"result": "failed", "message": "Missing Floor Number"})

    new_floor = models.Floor(number=floor_num)
    new_floor.save()

    return JsonResponse({"result": "success", "floor_id": new_floor.id})
	return JsonResponse({"result": "success", "data": {"floor_id": new_floor.id, "number": new_floor.number, "url": reverse("dashboard-floor-detail", args=new_floor.id)}})


def ajax_create_room(request):
	if not request.is_ajax():
		return JsonResponse({"result": "failed", "message": "Invalid Request"})

	floor_id = request.POST.get("floor-id", None)
	room_number = request.POST.get("room-number", None)
	room_size = request.POST.get("room-size", None)

	if not all([floor_id, room_number, room_size]):
		return JsonResponse({"result": "failed", "message": "Missing Data"})

	floor_data = core_utils.get_object_or_none(models.Floor, floor_id)

	if floor_data is None:
		return JsonResponse({"result": "failed", "message": "Unable to find floor with provided id: {}".format(floor_id)})

	new_room = models.Room(
		number=room_number,
		floor=floor_data,
		bed_count=0,
		size=room_size
	)
	new_room.save()

	new_room_data = serializers.RoomSerializer(new_room).data

	return JsonResponse({"result": "success", "data": new_room_data})


def ajax_create_bed(request):
	if not request.is_ajax():
		return JsonResponse({"result": "failed", "message": "Invalid Request"})

	bed_name = request.POST.get("name", None)
	bed_description = request.POST.get("description", None)

	if bed_name is None:
		return JsonResponse({"result": "failed", "message": "Missing Bed Name"})

	existing_bed = models.Bed.objects.filter(name=bed_name)
	if existing_bed:
		return JsonResponse({"result": "failed", "message": "A bed already exists with that name"})

	new_bed = models.Bed(name=bed_name, description=bed_description)
	new_bed.save()

	return JsonResponse({"result": "success", "data": {"bed_id": new_bed.id}})
