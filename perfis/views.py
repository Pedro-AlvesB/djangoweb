from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView, CreateView
from .forms import RegisterUserForm

# Create your views here.

class Login(LoginView):
    template_name = 'users/account/login.html'



class RegisterUser(FormView):
    model = User
    template_name = "users/account/register.html"
    form_class = RegisterUserForm
    success_url = "/perfis/register"

    def form_valid(self, form):
        print(form["password1"].value())
        user = form.save()
        return super().form_valid(form)
