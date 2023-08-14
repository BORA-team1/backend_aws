from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from audio.models import Playlist
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from django.db.models import Q

# Create your views here.
class IngDebateView(views.APIView):
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, cond__lt=3))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))
        lineseri=LineIngDebateSerializer(lines,many=True)
        return Response({"message": "진행중 투표 조회 성공", "data": {"Lines":lineseri.data}})


class DoneDebateView(views.APIView):
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, cond=3))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))     
        lineseri=LineDoneDebateSerializer(lines,many=True)
        return Response({"message": "완료된 투표 조회 성공", "data": {"Lines":lineseri.data}})

class MyDebateView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        debates=Debate.objects.filter(Q(debate_line__line_post=post_pk, debate_user=request.user.id))
        debates.order_by('debate_postsec__num','debate_line__sentence')  
        lines=list(set([debate.debate_line for debate in debates]))     
        lineseri=LineMyDebateSerializer(lines,many=True,context={'request': request})
        return Response({"message": "내가 만든 투표 조회 성공", "data": {"Lines":lineseri.data}})

class NewDebateView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, post_pk):
        first_cond=1
        user=request.user
        postsec=get_object_or_404(Line, line_id=request.data['debate_line'] ).line_postsec
        new_debate=NewDebateSerializer(data={
            'title': request.data['title'],
            'num':request.data['num'],
            'cond': first_cond,
            'debate_user':user.id,
            'debate_postsec':postsec.sec_id,
            'debate_line':request.data['debate_line']
        })
        if new_debate.is_valid():
            new_debate.save()
            return Response({"message": "토론 생성 성공", "data": new_debate.data})
        return Response({"message": "토론 생성 실패"})

class StartDebateView(views.APIView):
    def post(self, request, debate_pk):
        debate=get_object_or_404(Debate, debate_id=debate_pk)
        cons=[item['id'] for item in request.data['cons']]
        for con in cons:
            debate.cons.add(con)
            debate.debaters.add(con)
        pros=[item['id'] for item in request.data['pros']]
        for pro in pros:
            debate.pros.add(pro)
            debate.debaters.add(pro)
        
        debate.cond=2
        debate.save()

        seri=NewDebateSerializer(debate)
        
        return Response({"message": "토론 시작 성공", "data": seri.data})
    
class FinishDebateView(views.APIView):
    def patch(self, request, debate_pk):
        debate=get_object_or_404(Debate, debate_id=debate_pk)
        debate.cond=3
        debate.save()

        seri=NewDebateSerializer(debate)
        
        return Response({"message": "토론 종료 성공", "data": seri.data})
