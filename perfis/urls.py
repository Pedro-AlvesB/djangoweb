from django.urls import path
from .views import Login, RegisterUserForm

urlpatterns = [ 
    path('login/', Login.as_view(), name='login')
    path('registrar/' RegisterUserForm.as_view(), name='registrar')
]