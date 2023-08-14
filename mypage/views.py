from django.shortcuts import render,get_object_or_404
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from post.models import Post
from audio.models import Playlist, Audio
from account.serializers import UserProfileSerializer


# Create your views here.

class MyPageView(views.APIView):
    permission_classes = [IsAuthenticated]       # 현재 로그인한 사람 가져오려면 필요
    def get(self, request):
        # my 정보
        user=MyPageSerializer(request.user)      # 현재 로그인한 유저 정보 가져옴
        # 북마크한 Post
        now_user = request.user                                    # 현재 사용자   
        book_num=Post.objects.filter(bookmark=now_user.id).count()             
        book_posts= Post.objects.filter(bookmark=now_user.id)[:3]      # 현재 사용자를 bookmark에 가지고 있는 Post객체들을 필터링해서 가져옴
        for post in book_posts:                                     # 이 Post들의 is_booked는 True. 
            post.is_booked=True                                     # 이건 모델에 있는 정보가 아니라 우리가 상황에 따라 넘겨줘야 하는 정보니까 직접 적어준다
        bookmarkPost = BookPostSerializer(book_posts, many=True)    # BookPostSerializer에 Post객체 넣어서 시리얼라이저 형태에 맞게 만든다
    
        #팔로우
        follows_num=now_user.follow.count()
        follows=now_user.follow.all()[:6]
        followseri=UserProfileSerializer(follows,many=True)
        
        # 내 플레이리스트
        mypli_num=Playlist.objects.filter(mypli_user=now_user.id).count()
        myPli = Playlist.objects.filter(mypli_user=now_user.id)[:3]
        myPlaylist=MyPliSerializer(myPli,many=True)

        return Response({'message': '마이페이지 조회 성공', 'data': {'user': user.data,'book_num':book_num,'bookmarkPost':bookmarkPost.data,'follows_num':follows_num,'follows':followseri.data,'mypli_num':mypli_num,'myPlaylist':myPlaylist.data}}, status=status.HTTP_200_OK)

class BookmarkListView(views.APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        now_user = request.user
        book_posts= Post.objects.filter(bookmark=now_user.id)
        for post in book_posts:
            post.is_booked=True     
        bookmarkPost = BookPostSerializer(book_posts, many=True)
        return Response({'message': '북마크 목록 조회 성공', 'data': {'bookmarkPost':bookmarkPost.data}}, status=status.HTTP_200_OK)

class FollowListView(views.APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        now_user = request.user
        follows=now_user.follow.all()
        serializer = UserProfileSerializer(follows, many=True)
        return Response({'message': '팔로우 목록 조회 성공', 'data': {'follow':serializer.data}}, status=status.HTTP_200_OK)


class MypliListView(views.APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        now_user = request.user
        myPli = Playlist.objects.filter(mypli_user=now_user.id)
        myPlaylist=MyPliSerializer(myPli,many=True)
        return Response({'message': '재생목록 목록 조회 성공', 'data': {'myPlaylist':myPlaylist.data}}, status=status.HTTP_200_OK)
    
class FollowingView(views.APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, user_pk):
        user = request.user
        follow = get_object_or_404(User, id=user_pk)
        user.follow.add(follow)
        return Response({'message': '팔로우 성공'}, status=status.HTTP_200_OK)