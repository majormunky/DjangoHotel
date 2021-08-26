from django.shortcuts import render


def index(request):
	return render(request, "dashboard/index.html", {})


def floor_setup(request):
	return render(request, "dashboard/floor-setup.html", {})
