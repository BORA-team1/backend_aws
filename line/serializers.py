from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer


class MyLineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Line
        fields=['line_id','content']

class LineComComSerializer(serializers.ModelSerializer):
    linecomcom_user=UserProfileSerializer()
    is_my=serializers.SerializerMethodField(default=False)
    class Meta:
        model=LineComCom
        fields=['linecomcom_id','content','is_my','mention','linecomcom_user'] # related_name으로 쓰면 자동으로 중첩 시리얼라이저를 통해 역참조
    def get_is_my(self, obj):
        request = self.context.get('request')
        print(request)
        if request and request.user.is_authenticated:
            return obj.linecomcom_user == request.user
        return False
    

class MyLineComSerializer(serializers.ModelSerializer):
    do_like=serializers.SerializerMethodField(default=False)
    likenum=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField(default=False)
    LineComCom=LineComComSerializer(source='linecomcom_lineCom',many=True) # 역참조 할때 필드명은 LineComCom으로 하고싶으면 필드명은 바꾸고 source쓰면 된다
    linecom_user=UserProfileSerializer()
    class Meta:
        model=LineCom
        fields=['linecom_id','content','linecom_user','do_like','likenum','is_my','LineComCom']
    
    # 필요한 정보로 값 담기
    def get_likenum(self, obj):
        return obj.like.count()
    def get_do_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like.all()
        return False
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.linecom_user == request.user
        return False
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request:                                                     # is_my에서 requet.user가 필요하기 때문에 request넘기기 위해 to_representation함수
            linecomcom_data = LineComComSerializer(instance.linecomcom_lineCom.all(), many=True, context={'request': request}).data
            representation['LineComCom'] = linecomcom_data

        return representation
    

class MyLineandComSerializer(serializers.ModelSerializer):
    linecom_line = MyLineComSerializer(many=True, read_only=True)

    class Meta:
        model = Line
        fields = ['line_id', 'content', 'linecom_line']

    def to_representation(self, instance):                          # 현재 user의 LineCom만 가져오기위해 필터링
        request = self.context.get('request')   
        user = request.user                     

        queryset = instance.linecom_line.filter(linecom_user=user)
        serializer = MyLineComSerializer(queryset, many=True, context={'request': request}) # is_my, do_like를 위해 request를 넘겨야 함(현재 사용자가 누군지 알아야 하기 때문)
        # print(request.user)
        return {
            'line_id': instance.line_id,
            'content': instance.content,
            'LineCom': serializer.data
        }


class LineAnsSerializer(serializers.ModelSerializer):
    ans_user=UserProfileSerializer()
    class Meta:
        model=Answer
        fields=['ans_id','content','ans_user']

class MyLineQueSerializer(serializers.ModelSerializer):
    num=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField(default=False)
    Answer=LineAnsSerializer(source='ans_que',many=True) 
    que_user=UserProfileSerializer()
    class Meta:
        model=Question
        fields=['que_id','content','num','is_my','que_user','Answer']
    
    # 필요한 정보로 값 담기
    def get_num(self, obj):
        # return obj.like.count()
        ans=Answer.objects.filter(ans_que=obj)
        return ans.count()
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.que_user == request.user
        return False
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request:                                                     # is_my에서 requet.user가 필요하기 때문에 request넘기기 위해 to_representation함수
            ans_data = LineAnsSerializer(instance.ans_que.all(), many=True, context={'request': request}).data
            representation['Answer'] = ans_data

        return representation


class MyLineandQueSerializer(serializers.ModelSerializer):
    Question = MyLineQueSerializer(source='que_line',many=True, read_only=True)

    class Meta:
        model = Line
        fields = ['line_id', 'content', 'Question']

    def to_representation(self, instance):                  
        request = self.context.get('request')   
        user = request.user             
        representation = super().to_representation(instance)
        

        queryset = instance.que_line.filter(que_user=user)
        serializer = MyLineQueSerializer(queryset, many=True, context={'request': request}) 
        representation['Question'] = serializer.data  # 수정된 부분

        return representation


class MyLineEmoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Emotion
        fields=['emo_id','content']

class MyLineandEmoSerializer(serializers.ModelSerializer):
    Emotion = MyLineEmoSerializer(source='emo_line',many=True, read_only=True)

    class Meta:
        model = Line
        fields = ['line_id', 'content', 'Emotion']

    def to_representation(self, instance):                  
        request = self.context.get('request')   
        user = request.user             
        representation = super().to_representation(instance)
        

        queryset = instance.emo_line.filter(emo_user=user)
        serializer = MyLineEmoSerializer(queryset, many=True, context={'request': request}) 
        representation['Emotion'] = serializer.data  # 수정된 부분

        return representation
    
class LineComSerializer(serializers.ModelSerializer):
    linecom_user=UserProfileSerializer()
    do_like=serializers.SerializerMethodField()
    likenum=serializers.SerializerMethodField()
    LineComCom=LineComComSerializer(source='linecomcom_lineCom',many=True)
    is_my=serializers.SerializerMethodField()
    class Meta:
        model=LineCom
        fields=['linecom_id','content','linecom_user','do_like','likenum','is_my','LineComCom']

    def get_do_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like.all()
        return False
    def get_likenum(self, obj):
        return obj.like.count()
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.linecom_user == request.user
        return False
    
class NewLineComSerializer(serializers.ModelSerializer):
     class Meta:
        model=LineCom
        fields=['linecom_id','content','linecom_line','linecom_postsec','linecom_user']

class LineComLikeSerializer(serializers.ModelSerializer):
    do_like=serializers.SerializerMethodField()
    like_num=serializers.SerializerMethodField()
    class Meta:
        model=LineCom
        fields=['linecom_line','linecom_id','do_like','like_num']

    def get_do_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.like.all()
        return False
    def get_like_num(self, obj):
        return obj.like.count()


class NewLineComComSerializer(serializers.ModelSerializer):
    class Meta:
        model=LineComCom
        fields=['linecomcom_id','linecomcom_user','content','mention']

class AnswerSerializer(serializers.ModelSerializer):
    ans_user=UserProfileSerializer()
    class Meta:
        model=Answer
        fields=['ans_id','content','ans_user']

class QuestionSerializer(serializers.ModelSerializer):
    num=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField()
    que_user=UserProfileSerializer()
    Answer=AnswerSerializer(source='ans_que',many=True)
    class Meta:
        model=Question
        fields=['que_id','content','num','is_my','que_user','Answer']
    def get_num(self, obj):
        ans=Answer.objects.filter(ans_que=obj).all()
        return ans.count()
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.que_user == request.user
        return False



class NewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['que_id','content']

class NewAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['ans_id','content','ans_que','ans_user']

class NewEmoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Emotion
        fields=['emo_id','content','emo_line','emo_postsec','emo_user']

