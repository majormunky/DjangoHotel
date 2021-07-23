from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.contrib import messages
from . import forms

# Create your views here.
@login_required
def index(request):
    return render(request, "core/index.html", {})


def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)

        form = forms.CoreUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "Registration Successful!")
            return redirect("login")
        else:
            print(form.errors)
            return HttpResponseBadRequest("ERROR")
