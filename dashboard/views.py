from django.shortcuts import render, get_object_or_404
from rooms import models as room_models


def index(request):
	return render(request, "dashboard/index.html", {})


def floor_setup(request):
	floor_list = room_models.Floor.objects.all()
	return render(request, "dashboard/floor-setup.html", {"floor_list": floor_list})


def floor_detail(request, pk):
	room_size_choices = room_models.Room.SIZE_CHOICES
	floor_data = get_object_or_404(room_models.Floor, pk=pk)
	return render(
		request,
		"dashboard/floor-detail.html",
		{
			"floor_data": floor_data,
			"room_size_choices": room_size_choices,
		}
	)
