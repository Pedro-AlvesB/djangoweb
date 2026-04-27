from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterUserForm
from django.contrib.auth import login

# Create your views here.

class Login(LoginView):
    template_name = 'users/account/login.html'



class ContactFormView(FormView):
    template_name = "users/account/register.html"
    form_class = RegisterUserForm
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)