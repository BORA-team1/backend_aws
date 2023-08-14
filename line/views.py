from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from post.models import Post,PostSec
from line.models import Line
from .serializers import *


# Create your views here.

class MyLineView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user
        lines= Line.objects.filter(line_post=post).all()
        mylines= lines.filter(line_user=now_user).all()
        mylineseri=MyLineSerializer(mylines, many=True)
        return Response({'message': '내 밑줄 전체 조회 성공', 'data': {'Lines':mylineseri.data}}, status=status.HTTP_200_OK)
    
    def post(self, request, post_pk):
        now_user=request.user
        post= get_object_or_404(Post, post_id=post_pk)                                 # 현재 포스트 객체
        post_sec=get_object_or_404(PostSec, sec_id=request.data['line_postsec'])       # 현재 포스트 섹션
        sentence=request.data['sentence']
        content=request.data['content']
        line, created = Line.objects.get_or_create(line_post=post,line_postsec=post_sec,sentence=sentence)            # 현재 포스트의 섹션의 순번에 해당하는 line이 있으면 가져오고 없으면 만든다. 만들어졌다면 created=true
        line.content=content
        line.save()
        line.line_user.add(now_user)                                                   # 현재 사용자 추가
        return Response({'message': '밑줄 긋기 성공', 'data': {'line_id': line.line_id, 'sentence': line.sentence}}, status=status.HTTP_200_OK)

class MyLineComView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        linecoms1= LineCom.objects.filter(linecom_user=now_user).all()            # 사용자가 쓴 모든 LineCom
        linecoms= linecoms1.filter(linecom_line__line_post=post).all()            # 사용자의 LineCom중 현재 Post에 있는것만
        
        Lines=list(set([linecom.linecom_line for linecom in linecoms]))                      # 사용자의 LineCom이 있는 Line만

        seri=MyLineandComSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 댓글 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineQnAView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        que= Question.objects.filter(que_user=now_user).all()            
        questions= que.filter(que_line__line_post=post).all()           
        
        Lines=list(set([question.que_line for question in questions]))

        seri=MyLineandQueSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 Q&A 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineEmoView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        emo= Emotion.objects.filter(emo_user=now_user).all()            
        emotions= emo.filter(emo_line__line_post=post).all()           
        
        Lines=list(set([emotion.emo_line for emotion in emotions]))

        seri=MyLineandEmoSerializer(Lines,many=True, context={'request': request})  
        return Response({'message': '내 밑줄 감정표현 전체 조회 성공', 'data':{'Lines':seri.data}})

class MyLineDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        line.line_user.remove(request.user)
        return Response({"message": "내 밑줄 삭제 성공"})


class LineComView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, line_pk):
        line= get_object_or_404(Line, line_id=line_pk)
        linecoms=LineCom.objects.filter(linecom_line=line).all()
        serializer=LineComSerializer(linecoms,context={'request': request},many=True)
        return Response({'message': '밑줄 댓글 조회 성공', 'data': {'line_id':line.line_id,'content':line.content,'LineCom':serializer.data}}, status=status.HTTP_200_OK)

    def post(self, request, line_pk):
        line= get_object_or_404(Line, line_id=line_pk)
        now_user=request.user
        postsec=line.line_postsec
        serializer = NewLineComSerializer(data={
                    'content': request.data['content'],
                    'linecom_line': line_pk,
                    'linecom_postsec': postsec.sec_id,
                    'linecom_user': now_user.id
                })
        if serializer.is_valid():
            serializer.save()   
            return Response({'message':'밑줄 댓글 등록 성공','data':{'linecom_line':serializer.data['linecom_line'],'linecom_id':serializer.data['linecom_id'],'linecom_user':serializer.data['linecom_user'],"content":serializer.data['content']}}, status=status.HTTP_201_CREATED)
        return Response({'message':'밑줄 댓글 등록 실패','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class LineCom2View(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_pk):
        postsec=request.data['line_postsec']
        sentence=request.data['sentence']

        try:
            line = Line.objects.get(line_post=post_pk, line_postsec=postsec, sentence=sentence)
        except Line.DoesNotExist:
            return Response({'message': '이 문장에 해당하는 댓글이 없습니다!'}, status=status.HTTP_404_NOT_FOUND)

        linecoms=LineCom.objects.filter(linecom_line=line).all()
        serializer=LineComSerializer(linecoms,context={'request': request},many=True)
        return Response({'message': '밑줄 댓글 조회 성공!', 'data': {'line_id':line.line_id,'content':line.content,'LineCom':serializer.data}}, status=status.HTTP_200_OK)

    def post(self, request, post_pk):
        postsec=get_object_or_404(PostSec, sec_id=request.data['line_postsec'])
        sentence=request.data['sentence']
        line_content=request.data['line_content']
        content=request.data['content']
        post= get_object_or_404(Post, post_id=post_pk)

        line,created= Line.objects.get_or_create(line_post=post,line_postsec=postsec,sentence=sentence)
        if created: 
            line.content=line_content
            line.save()

        now_user=request.user
        postsec=line.line_postsec
        serializer = NewLineComSerializer(data={
                    'content': content,
                    'linecom_line': line.line_id,
                    'linecom_postsec': postsec.sec_id,
                    'linecom_user': now_user.id
                })
        if serializer.is_valid():
            serializer.save()   
            return Response({'message':'밑줄 댓글 등록 성공!','data':{'linecom_line':serializer.data['linecom_line'],'linecom_id':serializer.data['linecom_id'],'linecom_user':serializer.data['linecom_user'],"content":serializer.data['content']}}, status=status.HTTP_201_CREATED)
        return Response({'message':'밑줄 댓글 등록 실패!','error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    
class DeleteComView(views.APIView):
    def delete(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.delete()
        return Response({"message": "밑줄 댓글 삭제 성공"})

class LineComLikeView(views.APIView):
    def post(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.like.add(request.user)
        serializer=LineComLikeSerializer(linecom,context={'request': request})
        return Response({"message": "밑줄 댓글 좋아요 성공","data":serializer.data})
    def delete(self,request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        linecom.like.remove(request.user)
        serializer=LineComLikeSerializer(linecom,context={'request': request})
        return Response({"message": "밑줄 댓글 좋아요 취소 성공","data":serializer.data})

class NewLineComComView(views.APIView):
    def post(self, request, linecom_pk):
        linecom=get_object_or_404(LineCom,linecom_id=linecom_pk)
        newcomcom=NewLineComComSerializer(data={'content':request.data['content'],'mention':request.data['mention'],'linecomcom_user':request.user.id})
        if newcomcom.is_valid():
            newcomcom.save(linecomcom_lineCom=linecom)   # 시리얼라이저 필드에 없는 값 추가
            return Response({'message':'밑줄 댓글 답글 등록 성공','data':newcomcom.data}, status=status.HTTP_201_CREATED)
        return Response({'message':'밑줄 댓글 답글 작성 실패','error':newcomcom.errors},status=status.HTTP_400_BAD_REQUEST)

class DeleteComComView(views.APIView):
    def delete(self, request, linecomcom_pk):
        linecomcom=get_object_or_404(LineComCom,linecomcom_id=linecomcom_pk)
        linecomcom.delete()
        return Response({"message": "밑줄 댓글 답글 삭제 성공"})

class LineQnAView(views.APIView):
    def post(self, request, line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        postsec=line.line_postsec
        now_user=request.user
        newQue=NewQuestionSerializer(data=request.data)
        if newQue.is_valid():
            newQue.save(que_line=line,que_postsec=postsec,que_user=now_user)
            return Response({"message": "밑줄 Q&A 등록 성공","data":{"que_line":line.line_id,"que_id":newQue.data['que_id'],'que_user':now_user.id,"content":newQue.data['content']}})
    def get (self, request, line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        ques=Question.objects.filter(que_line=line).all()
        queseri=QuestionSerializer(ques,many=True,context={'request': request})
        return Response({"message": "밑줄 Q&A 조회 성공","data":{"line_id":line.line_id,"content":line.content,'Question':queseri.data}})

class LineQnA2View(views.APIView):
    def post(self, request, post_pk):
        postsec=get_object_or_404(PostSec, sec_id=request.data['line_postsec'])
        sentence=request.data['sentence']
        line_content=request.data['line_content']
        content=request.data['content']
        post= get_object_or_404(Post, post_id=post_pk)

        line,created= Line.objects.get_or_create(sentence=sentence,line_post=post,line_postsec=postsec)
        if created: 
            line.content=line_content
            line.save()

        now_user=request.user
        newQue=NewQuestionSerializer(data=request.data)
        if newQue.is_valid():
            newQue.save(que_line=line,que_postsec=postsec,que_user=now_user)
            return Response({"message": "밑줄 Q&A 등록 성공!","data":{"que_line":line.line_id,"que_id":newQue.data['que_id'],'que_user':now_user.id,"content":newQue.data['content']}})
    def get (self, request, post_pk):
        postsec=request.data['line_postsec']
        sentence=request.data['sentence']
        try:
            line = Line.objects.get(line_post=post_pk, line_postsec=postsec, sentence=sentence)
        except Line.DoesNotExist:
            return Response({'message': '이 문장에 해당하는 질문이 없습니다!'}, status=status.HTTP_404_NOT_FOUND)

        ques=Question.objects.filter(que_line=line).all()
        queseri=QuestionSerializer(ques,many=True,context={'request': request})
        return Response({"message": "밑줄 Q&A 조회 성공!","data":{"line_id":line.line_id,"content":line.content,'Question':queseri.data}})


class DeleteQueView(views.APIView):
    def delete (self, request, question_pk):
        que=get_object_or_404(Question,que_id=question_pk)
        que.delete()
        return Response({"message": "밑줄 Q&A 삭제 성공"})

class AnswerView(views.APIView):
    def post(self, request,question_pk):
        ansseri=NewAnswerSerializer(data={'content':request.data['content'],'ans_user':request.user.id,'ans_que':question_pk})
        if ansseri.is_valid():
            ansseri.save()
            return Response({"message": "밑줄 Q&A 답변 등록 성공","data":ansseri.data})
        else:
            return Response({"message": "밑줄 Q&A 답변 등록 실패","error":ansseri.errors},status=status.HTTP_400_BAD_REQUEST)
    
class EmoView(views.APIView):
    def post(self, request,line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        content=request.data['content']
        postsec=line.line_postsec
        now_user=request.user
        if Emotion.objects.filter(emo_line=line_pk,emo_user=now_user.id,content=content).exists() :
            return Response({"message": "이미 존재하는 감정표현입니다 "})
        emo=NewEmoSerializer(data={
            'content':content,
            'emo_line':line.line_id,
            'emo_postsec':postsec.sec_id,
            'emo_user':now_user.id
        })
        if emo.is_valid():
            emo.save()
            return Response({"message": "밑줄 감정표현 등록 성공","data":emo.data})
        else:
            return Response({"message": "밑줄 감정표현 등록 실패","error":emo.errors},status=status.HTTP_400_BAD_REQUEST)
    def get (self, request,line_pk):
        line=get_object_or_404(Line,line_id=line_pk)
        emos=Emotion.objects.filter(emo_line=line).all()  
        is_my_1,is_my_2,is_my_3,is_my_4,is_my_5 =[False] * 5
        
        emo1s=emos.filter(content=1).all()
        emo1count=emo1s.count()
        for emo in emo1s:
            if emo.emo_user==request.user : is_my_1=True

        emo2s=emos.filter(content=2).all()
        emo2count=emo2s.count()
        for emo in emo2s:
            if emo.emo_user==request.user : is_my_2=True
        
        emo3s=emos.filter(content=3).all()
        emo3count=emo3s.count()
        for emo in emo3s:
            if emo.emo_user==request.user : is_my_3=True

        emo4s=emos.filter(content=4).all()
        emo4count=emo4s.count()
        for emo in emo4s:
            if emo.emo_user==request.user : is_my_4=True

        emo5s=emos.filter(content=5).all()
        emo5count=emo5s.count()
        for emo in emo5s:
            if emo.emo_user==request.user : is_my_5=True
        
        data = {
                'line_id': line_pk,
                'content': line.content,
                'Emotion': [
                    {'content': 1, 'num': emo1count, 'is_my': is_my_1},
                    {'content': 2, 'num': emo2count, 'is_my': is_my_2},
                    {'content': 3, 'num': emo3count, 'is_my': is_my_3},
                    {'content': 4, 'num': emo4count, 'is_my': is_my_4},
                    {'content': 5, 'num': emo5count, 'is_my': is_my_5},
                ],
            }

        return Response({'message':"밑줄 감정표현 조회 성공","data":data})
    def delete(self, request,line_pk):
        content=request.data['content']
        line=get_object_or_404(Line,line_id=line_pk)
        now_user=request.user
        emo=Emotion.objects.filter(emo_line=line_pk,emo_user=now_user.id,content=content) 
        emo.delete()
        return Response({"message": "밑줄 감정표현 삭제 성공"})
    
class LineEmo2View(views.APIView):
    def post(self, request,post_pk):
        postsec=get_object_or_404(PostSec, sec_id=request.data['line_postsec'])
        sentence=request.data['sentence']
        line_content=request.data['line_content']
        content=request.data['content']
        post= get_object_or_404(Post, post_id=post_pk)
        now_user=request.user

        line,created= Line.objects.get_or_create(sentence=sentence,line_post=post,line_postsec=postsec)
        if created: 
            line.content=line_content
            line.save()

        
        if Emotion.objects.filter(emo_line=line.line_id,emo_user=now_user.id,content=content).exists() :
            return Response({"message": "이미 존재하는 감정표현입니다 "})
        emo=NewEmoSerializer(data={
            'content':content,
            'emo_line':line.line_id,
            'emo_postsec':postsec.sec_id,
            'emo_user':now_user.id
        })
        if emo.is_valid():
            emo.save()
            return Response({"message": "밑줄 감정표현 등록 성공!","data":emo.data})
        else:
            return Response({"message": "밑줄 감정표현 등록 실패!","error":emo.errors},status=status.HTTP_400_BAD_REQUEST)
    def get (self, request,post_pk):
        postsec=request.data['line_postsec']
        sentence=request.data['sentence']
        try:
            line = Line.objects.get(line_post=post_pk, line_postsec=postsec, sentence=sentence)
        except Line.DoesNotExist:
            return Response({'message': '이 문장에 해당하는 감정표현이 없습니다!'}, status=status.HTTP_404_NOT_FOUND)

        emos=Emotion.objects.filter(emo_line=line).all()  
        is_my_1,is_my_2,is_my_3,is_my_4,is_my_5 =[False] * 5
        
        emo1s=emos.filter(content=1).all()
        emo1count=emo1s.count()
        for emo in emo1s:
            if emo.emo_user==request.user : is_my_1=True

        emo2s=emos.filter(content=2).all()
        emo2count=emo2s.count()
        for emo in emo2s:
            if emo.emo_user==request.user : is_my_2=True
        
        emo3s=emos.filter(content=3).all()
        emo3count=emo3s.count()
        for emo in emo3s:
            if emo.emo_user==request.user : is_my_3=True

        emo4s=emos.filter(content=4).all()
        emo4count=emo4s.count()
        for emo in emo4s:
            if emo.emo_user==request.user : is_my_4=True

        emo5s=emos.filter(content=5).all()
        emo5count=emo5s.count()
        for emo in emo5s:
            if emo.emo_user==request.user : is_my_5=True
        
        data = {
                'line_id': line.line_id,
                'content': line.content,
                'Emotion': [
                    {'content': 1, 'num': emo1count, 'is_my': is_my_1},
                    {'content': 2, 'num': emo2count, 'is_my': is_my_2},
                    {'content': 3, 'num': emo3count, 'is_my': is_my_3},
                    {'content': 4, 'num': emo4count, 'is_my': is_my_4},
                    {'content': 5, 'num': emo5count, 'is_my': is_my_5},
                ],
            }

        return Response({'message':"밑줄 감정표현 조회 성공!","data":data})
    def delete(self, request,post_pk):
        postsec=request.data['line_postsec']
        sentence=request.data['sentence']
        content=request.data['content']

        line = get_object_or_404(Line, line_post=post_pk, line_postsec=postsec, sentence=sentence)
        
        now_user=request.user
        emo=Emotion.objects.filter(emo_line=line.line_id,emo_user=now_user.id,content=content) 
        emo.delete()
        return Response({"message": "밑줄 감정표현 삭제 성공!"})




    
