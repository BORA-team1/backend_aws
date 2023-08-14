from django.contrib import admin
from django.urls import path
from .views import *

app_name='post'      

urlpatterns = [
    path('search/',SearchView.as_view()),
    path('',MainView.as_view()),
    path('lists/',PostListView.as_view()),
    path('<int:post_pk>/bookmark/',BookMarkView.as_view()),
    path('<int:post_pk>/',PostDetailView.as_view()),
    path('<int:post_pk>/contents/',PostAllContentView.as_view())
]
