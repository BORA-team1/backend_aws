from django.contrib import admin
from django.urls import path
from .views import *

app_name='audio'      

urlpatterns = [
    path('<int:audio_pk>/<int:playlist_pk>/',AudioDetailView.as_view()),
    path('<int:playlist_pk>/',PlaylistView.as_view()),
    path('new/',NewPlaylistView.as_view()),
]