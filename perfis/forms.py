from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterUserForm(UserCreationForm):
    class meta:
        model = CustomUser
        field = ('username', 'email', 'password1', 'password2')
        