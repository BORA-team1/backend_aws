from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *


from .models import *
from .serializers import *
# Create your views here.

#한마디 조회/작성/삭제
class HanView(views.APIView):
    permission_classes = [IsAuthenticated]  
    #한마디 조회
    def get(self, request, post_pk): 
        user = request.user                    
        hans=Han.objects.filter(han_post=post_pk).all()
        
        for han in hans:
            if han.like.filter(pk=user.id).exists():
                han.do_like=True
            han.like_num=han.like.count()
            if han.han_user==user:
                han.is_my=True

        serializer = HanSerializer(hans,many=True)           #인스턴스 생성 시 han 전달     
        return Response({'message': '한마디 조회 성공', 'data': {"han": serializer.data}}, status=status.HTTP_200_OK)
    
    #한마디 등록
    def post(self, request, post_pk):
        hans=Han.objects.filter(han_post=post_pk).all()
        data = {
            'han_user' : request.user.id,
            'content' : request.data['content'],
            'han_post': post_pk
        }
        serializer = NewHanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '한마디 작성 성공', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '한마디 작성 실패', 'data': serializer.error}, status=status.HTTP_400_BAD_REQUEST)

class HanDelView(views.APIView):
    #한마디 삭제
    def delete(self, request, han_pk):
        han=get_object_or_404(Han, han_id = han_pk)
        han.delete()

        return Response({'message' : '한마디 삭제 성공'}, status=status.HTTP_204_NO_CONTENT)


#한마디 추천 관련 view
class HanRecommendView(views.APIView):
    serializer_class = NewHanSerializer
    permission_classes = [IsAuthenticated] 
    #한마디 추천
    def post(self, request, han_pk):
        han_user = request.user
        han = get_object_or_404(Han, han_id=han_pk)                     #han_post가 맞나
        serializer = self.serializer_class(han)
        if han.like.filter(id=han_user.id).exists():
            han.like.remove(han_user)
            return Response({'message': '한마디 추천 취소 성공', 'data': {'han': serializer.data}}, status=status.HTTP_200_OK)
        else:
            han.like.add(han_user)                                          #좋아요 취소가 가능하니 유저 정보 넘겨줘야겠지?
            return Response({'message': '한마디 추천 성공', 'data': {'han': serializer.data}}, status=status.HTTP_200_OK)
        return Response({'message': '한마디 추천 취소 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # 한마디 추천 여부 변경으로 합침
    # #한마디 추천 취소
    # def delete(self, request, han_pk):
    #     han_user = request.user #한마디 추천과 동일
    #     han = get_object_or_404(Han, pk=han_pk) 
    #     han.like.remove(han_user)

    #     # serializer = self.serializer_class(data=request.data, instance=han, partial=True)     
    #     serializer = self.serializer_class(han)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': '한마디 추천 취소 성공', 'data': {'han': serializer.data}}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'message': '한마디 추천 취소 실패', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#한마디 답글
class HanComView(views.APIView):
    permission_classes = [IsAuthenticated] 
    #한마디 답글 달기
    def post(self, request, han_pk):
        hancom=NewHanComSerializer(data={'content':request.data['content'],'mention':request.data['mention'],'hancom_user':request.user.id,'hancom_han':han_pk})

        if hancom.is_valid():
            hancom.save()  
            return Response({'message':'한마디 답글 작성 성공','data':hancom.data}, status=status.HTTP_200_OK)
        return Response({'message':'한마디 답글 작성 실패','error':hancom.errors},status=status.HTTP_400_BAD_REQUEST)
    
    
class HanComDelView(views.APIView):
    #한마디 답글 삭제
    def delete(self, request, hancom_pk):
        hancom=get_object_or_404(HanCom,hancom_id=hancom_pk)
        hancom.delete()
        return Response({"message": " 한마디 답글 삭제 성공"})