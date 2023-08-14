from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer,InterestSerializer
from audio.models import Playlist
from line.models import Line, LineCom, Question, Emotion, Answer,LineComCom
from vote.models import Vote, VotePer
from debate.models import Debate
from han.models import Han
from django.db.models import Count
from rest_framework import serializers



class PostSearchSerializer(serializers.ModelSerializer):
    is_vote = serializers.BooleanField(default=False)
    is_debate = serializers.BooleanField(default=False)
    is_que = serializers.BooleanField(default=False)
    hashtag=InterestSerializer(many=True, read_only=True)
    author=serializers.CharField(default=False)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','hashtag', 'author', 'is_vote' ,'is_debate','is_que']

class PostBoxSerializer(serializers.ModelSerializer):
    is_booked = serializers.BooleanField(default=False)
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','diff','is_booked','hashtag']

class PliSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=Playlist
        fields=['playlist_id','title','hashtag','first_audio']

class PostDetailSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    author=serializers.CharField(default=False)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','diff','author','date','hashtag']

#-------------세부 포스트----------------

class LineComPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineCom
        fields=['linecom_id']

class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields=['que_id']

class IngVotePostSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    class Meta:
        model = Vote
        fields=['vote_id','title','vote_user']

class DoneVotePostSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    result=serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields=['vote_id','title','item1', 'item2', 'item3', 'start_date','done_date','vote_user','result']
    def get_result(self, instance):
        result = {}  # 결과를 저장할 딕셔너리
        for age, _ in VotePer.AGES:
            for select, _ in VotePer.SELECTS:
                result[f"result{select}_{age}"] = VotePer.objects.filter(voteper_vote=instance, age=age, select=select).count()
        return result
    
class DebatePostSerializer(serializers.ModelSerializer):
    debate_user=UserProfileSerializer(many=True,source='debaters')
    class Meta:
        model = Debate
        fields = ['debate_id', 'title', 'cond','debate_user']

class LineSerializer(serializers.ModelSerializer):
    LineCom = LineComPostSerializer(many=True,source='linecom_line')
    Question = QuestionPostSerializer(many=True, source='que_line')
    Emotion =serializers.SerializerMethodField()
    IngVote=serializers.SerializerMethodField()
    DoneVote=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField()
    Debate=DebatePostSerializer(many=True, source='debate_line')
    
    class Meta:
        model = Line
        fields = ['line_id', 'sentence', 'content', 'is_my', 'LineCom', 'Question', 'Emotion', 'IngVote', 'DoneVote','Debate']

    def get_is_my(self, obj):
        request = self.context.get('request')
        if request.user in obj.line_user.all():
            return True
        else:
            return False
    
    def get_IngVote(self, obj):
        ing_votes = obj.vote_line.filter(is_done=False)
        serializer = IngVotePostSerializer(ing_votes, many=True)
        return serializer.data

    def get_DoneVote(self, obj):
        done_votes = obj.vote_line.filter(is_done=True)
        serializer = DoneVotePostSerializer(done_votes, many=True)
        return serializer.data
    
    def get_Emotion(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        
        # 해당 Line에 연결된 Emotion 중에서 content별로 사용자 수를 계산
        emotion_counts = Emotion.objects.filter(emo_line_id=line_id).values('content').annotate(num=Count('emo_id'))
        
        # content 순서에 따라 결과를 만들기 위해 딕셔너리로 변환
        emotion_count_dict = {item['content']: item['num'] for item in emotion_counts}
        
        # 모든 content에 대해 결과를 생성하며, 없으면 기본값인 0 사용
        result = [
            {'content': content, 'num': emotion_count_dict.get(content, 0)}
            for content in range(1, 6)  # content는 1부터 5까지의 숫자
        ]
        
        return EmotionCountSerializer(result, many=True, context={'request': request, 'line': line_id}).data


class PostSecSerializer(serializers.ModelSerializer):
    Lines=LineSerializer(many=True,source='line_postsec')
    class Meta:
        model=PostSec
        fields=['sec_id','num','title','content','Lines']
    def to_representation(self, instance):                  
        request = self.context.get('request')   
        representation = super().to_representation(instance)
        lines = instance.line_postsec.all().order_by('sentence')

        serializer = LineSerializer(lines, many=True, context={'request': request},source='line_postsec') 
        representation['Lines'] = serializer.data

        return representation
    

class HanSerializer(serializers.ModelSerializer):
    han_user=UserProfileSerializer()
    like_num=serializers.SerializerMethodField()
    do_like=serializers.SerializerMethodField()
    
    class Meta:
        model=Han
        fields=['han_id','content', 'do_like', 'like_num','han_user']

    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.que_user == request.user
        return False
    def get_do_like(self, obj):
        request = self.context.get('request')
        if request.user in obj.like.all():
            return True
        else:
            return False
    def get_like_num(self, obj):
        return obj.like.count()
    

#-------------콘텐츠 모아보기----------------
class LineComComContentSerializer(serializers.ModelSerializer):
    linecomcom_user=UserProfileSerializer()
    is_my=serializers.SerializerMethodField()
    class Meta:
        model = LineComCom
        fields=['linecomcom_id','content','is_my','mention','linecomcom_user']
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.linecomcom_user == request.user
        return False
    

class LineComContentSerializer(serializers.ModelSerializer):
    linecom_user=UserProfileSerializer()
    LineComCom=LineComComContentSerializer(many=True,source='linecomcom_lineCom')
    do_like=serializers.SerializerMethodField()
    likenum=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField()
    class Meta:
        model = LineCom
        fields=['linecom_id','content','linecom_user','do_like','likenum','is_my','LineComCom']
    def get_likenum(self, obj):
        return obj.like.count()
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.linecom_user == request.user
        return False
    def get_do_like(self, obj):
        request = self.context.get('request')
        if request.user in obj.like.all():
            return True
        else:
            return False
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        serializer = LineComComContentSerializer(instance.linecomcom_lineCom, many=True, context={'request': request})
        representation['LineComCom'] = serializer.data

        return representation


class AnswerContentSerializer(serializers.ModelSerializer):
    ans_user=UserProfileSerializer()
    class Meta:
        model = Answer
        fields=['ans_id', 'content', 'ans_user']

class QuestionContentSerializer(serializers.ModelSerializer):
    Answer=AnswerContentSerializer(many=True,source='ans_que')
    que_user=UserProfileSerializer()
    num=serializers.SerializerMethodField()
    is_my=serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields=['que_id','content','num','que_user','is_my','Answer']
    def get_num(self, obj):
        return Answer.objects.filter(ans_que=obj.que_id).count()
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.que_user == request.user
        return False

class EmotionCountSerializer(serializers.Serializer):
    content = serializers.IntegerField()
    num = serializers.IntegerField()
    is_my = serializers.SerializerMethodField()
    def get_is_my(self, obj):
        request = self.context.get('request')
        line=self.context.get('line')
        user=request.user
        if request and request.user.is_authenticated:
            if Emotion.objects.filter(content=obj['content'], emo_user=user,emo_line=line).exists():
                return True
            else:
                return False
        return False
    
    
class DebateContentSerializer(serializers.ModelSerializer):
    debate_user=UserProfileSerializer()
    debaters=UserProfileSerializer(many=True)
    class Meta:
        model = Debate
        fields = ['debate_id', 'title','num', 'cond','debate_user','debaters']

class LineContentSerializer(serializers.ModelSerializer):
    LineCom = LineComContentSerializer(many=True,source='linecom_line')
    Question = QuestionContentSerializer(many=True, source='que_line')
    Emotion = serializers.SerializerMethodField()
    IngVote=serializers.SerializerMethodField()
    DoneVote=serializers.SerializerMethodField()
    Debate=DebateContentSerializer(many=True, source='debate_line')
    
    class Meta:
        model = Line
        fields = ['line_id', 'sentence', 'content','LineCom', 'Question', 'Emotion', 'IngVote', 'DoneVote','Debate']

    def get_IngVote(self, obj):
        ing_votes = obj.vote_line.filter(is_done=False)
        serializer = IngVotePostSerializer(ing_votes, many=True)
        return serializer.data

    def get_DoneVote(self, obj):
        done_votes = obj.vote_line.filter(is_done=True)
        serializer = DoneVotePostSerializer(done_votes, many=True)
        return serializer.data
    
    def get_Emotion(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        
        # 해당 Line에 연결된 Emotion 중에서 content별로 사용자 수를 계산
        emotion_counts = Emotion.objects.filter(emo_line_id=line_id).values('content').annotate(num=Count('emo_id'))
        
        # content 순서에 따라 결과를 만들기 위해 딕셔너리로 변환
        emotion_count_dict = {item['content']: item['num'] for item in emotion_counts}
        
        # 모든 content에 대해 결과를 생성하며, 없으면 기본값인 0 사용
        result = [
            {'content': content, 'num': emotion_count_dict.get(content, 0)}
            for content in range(1, 6)  # content는 1부터 5까지의 숫자
        ]
        
        return EmotionCountSerializer(result, many=True, context={'request': request, 'line': line_id}).data


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        serializer = QuestionContentSerializer(instance.que_line, many=True, context={'request': request})
        representation['Question'] = serializer.data

        serializer2= LineComContentSerializer(instance.linecom_line,many=True, context={'request': request})
        representation['LineCom']= serializer2.data


        return representation


class PostSecContentSerializer(serializers.ModelSerializer):
    Lines=LineContentSerializer(many=True,source='line_postsec')
    class Meta:
        model=PostSec
        fields=['sec_id','num','Lines']
    def to_representation(self, instance):                  
        request = self.context.get('request')   
        representation = super().to_representation(instance)
        lines = instance.line_postsec.all().order_by('sentence')

        serializer = LineContentSerializer(lines, many=True, context={'request': request},source='line_postsec') 
        representation['Lines'] = serializer.data

        return representation
    
