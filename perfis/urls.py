from django.urls import path
from .views import Login, RegisterUser
from . import views

urlpatterns = [ 
    path('login/', Login.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
]