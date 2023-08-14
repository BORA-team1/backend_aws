from django.contrib import admin
from django.urls import path
from .views import *

app_name='han'      

urlpatterns = [
    path('<int:post_pk>/',HanView.as_view()), #한마디 조회/등록
    path('delete/<int:han_pk>/',HanDelView.as_view()),
    path('like/<int:han_pk>/',HanRecommendView.as_view()), #한마디 추천/추천 취소
    path('com/<int:han_pk>/',HanComView.as_view()), #한마디 답글 달기
    path('com/del/<int:hancom_pk>/',HanComDelView.as_view()) #한마디 답글 삭제     
]
#한마디 조회/등록/삭제/추천/추천취소/답글달기/답글삭제
