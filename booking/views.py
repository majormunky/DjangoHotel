from django.shortcuts import render


def book_room(request):
    return render(request, "booking/book-room.html", {})
