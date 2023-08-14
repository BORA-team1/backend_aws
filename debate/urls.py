from django.contrib import admin
from django.urls import path
from .views import *

app_name='debate'      

urlpatterns = [
    path('ing/<int:post_pk>/',IngDebateView.as_view()),
    path('done/<int:post_pk>/',DoneDebateView.as_view()),
    path('my/<int:post_pk>/',MyDebateView.as_view()),
    path('<int:post_pk>/',NewDebateView.as_view()),
    path('start/<int:debate_pk>/',StartDebateView.as_view()),
    path('finish/<int:debate_pk>/',FinishDebateView.as_view())
]