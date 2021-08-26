from django.shortcuts import render
from rooms import models as room_models


def index(request):
	return render(request, "dashboard/index.html", {})


def floor_setup(request):
	floor_list = room_models.Floor.objects.all()
	return render(request, "dashboard/floor-setup.html", {"floor_list": floor_list})
