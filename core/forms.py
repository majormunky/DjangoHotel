from django.contrib.auth.forms import UserCreationForm
from .models import CoreUser


class CoreUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CoreUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
