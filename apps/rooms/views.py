from django.shortcuts import render


def index(request):
	return render(request, "rooms/index.html", {})


def setup(request):
	return render(request, "rooms/setup.html", {})
