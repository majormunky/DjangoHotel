from django.shortcuts import render
from django.http import JsonResponse
from . import models


def index(request):
	return render(request, "rooms/index.html", {})


def setup(request):
	return render(request, "rooms/setup.html", {})


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
