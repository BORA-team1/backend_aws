from django.contrib import admin
from django.urls import path
from .views import *

app_name='account'      

urlpatterns = [
    path('signup/',SignUpView.as_view()),
    path('login/',LoginView.as_view()),
    path('me/',MyProfileView.as_view())
]