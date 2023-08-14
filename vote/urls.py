from django.contrib import admin
from django.urls import path
from .views import *

app_name='vote'      

urlpatterns = [
    path('<int:post_pk>/',VoteCreateView.as_view()), #투표 등록
    path('voting/<int:vote_pk>/',VoteView.as_view()), #투표하기
    path('ing/<int:post_pk>/',VoteIngView.as_view()), #진행중인 투표 조회
    path('done/<int:post_pk>/',DoneVoteView.as_view()), #완료된 투표 조회 #post_pk 사용 시 계속 에러 발생으로 그냥 pk로 변경
    path('my/<int:post_pk>/',MyCreatingVoteView.as_view()), #내가 만든 투표 조회
    path('finish/<int:vote_pk>/',VoteFinishView.as_view()) #내가 만든 투표 종료
    
]