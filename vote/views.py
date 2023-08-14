from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .models import *
from .serializers import *
from line.models import Line

# Create your views here.


class VoteCreateView(views.APIView):
    #투표 등록
    def post(self, request, post_pk):
        data = request.data
        data['vote_user'] = request.user.id             #현재 로그인한 사용자를 투표 작성자로 설정
        data['vote_post'] = post_pk
        postsec=get_object_or_404(Line, line_id=data['vote_line']).line_postsec.sec_id
        data['vote_postsec'] = postsec

        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "투표 작성 성공","data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VoteView(views.APIView):
    #투표하기
    def post(self, request, vote_pk):
        try:
            vote = Vote.objects.get(vote_id=vote_pk)
        except Vote.DoesNotExist:
            return Response({'message': '투표가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        vote_per, created= VotePer.objects.get_or_create(voteper_user=user, voteper_vote=vote) 
        if created: 
            vote_per.age=user.age
            
        if request.data['select'] not in [1,2,3]:
            return Response({'message': '유효하지 않은 항목입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        vote_per.select=request.data['select']
        vote_per.save()
        return Response({'message': '투표 완료'}, status=status.HTTP_201_CREATED)

class VoteIngView(views.APIView):
    #진행중인 투표 조회
    serializer_class = VoteSerializer

    def get(self, request, post_pk):
        post=get_object_or_404(Post, post_id=post_pk)
        votes=Vote.objects.filter(vote_post=post.post_id,is_done=False).all()
        lines=list(set([vote.vote_line for vote in votes]))   
        
        seri=IngVoteLineSerializer(lines,many=True, context={'request': request}) 

        return Response({"message": "진행중 투표 조회 성공", "data": {"Lines":seri.data}}, status=status.HTTP_200_OK)
    
    
class DoneVoteView(views.APIView):
    #완료된 투표 조회
    serializer_class = DoneVoteSerializer
    #lookup_field = 'post_pk'
    def get(self, request, post_pk):
        post=get_object_or_404(Post, post_id=post_pk)
        votes=Vote.objects.filter(vote_post=post.post_id,is_done=True).all()
        lines=list(set([vote.vote_line for vote in votes]))   
        
        seri=DoneVoteLineSerializer(lines,many=True, context={'request': request}) 

        return Response({"message": "완료된 투표 조회 성공", "data": {"Lines":seri.data}}, status=status.HTTP_200_OK)

class MyCreatingVoteView(views.APIView):
    #내가 만든 투표 조회
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        user = self.request.user
        post=get_object_or_404(Post, post_id=post_pk)
        votes=Vote.objects.filter(vote_post=post.post_id,vote_user=user.id).all()
        lines=list(set([vote.vote_line for vote in votes]))   
        
        seri=MyVoteLineSerializer(lines,many=True, context={'request': request}) 

        return Response({"message": "내가 만든 투표 조회 성공", "data": {"Lines":seri.data}}, status=status.HTTP_200_OK)

class VoteFinishView(views.APIView):
    #내가 만든 투표 종료
    def patch(self, request, vote_pk):
        vote = get_object_or_404(Vote, vote_id=vote_pk, vote_user=request.user)
        vote.is_done = True
        vote.save()

        serializer = VoteSerializer(vote)

        return Response({"message": "투표 종료 성공", "data": serializer.data}, status=status.HTTP_200_OK)