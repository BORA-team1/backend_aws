from django.contrib import admin
from django.urls import path
from .views import *

app_name='mypage'      

urlpatterns = [
    path('',MyPageView.as_view()),
    path('bookmark/',BookmarkListView.as_view()),
    path('follow/',FollowListView.as_view()),
    path('mypli/',MypliListView.as_view()),
    path('following/<int:user_pk>/',FollowingView.as_view())
]