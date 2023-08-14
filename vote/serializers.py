from rest_framework import serializers
from .models import *
from account.serializers import UserProfileSerializer

class VoteSerializer(serializers.ModelSerializer):
    # vote_user=UserProfileSerializer()
    class Meta:
        model = Vote
        fields = ['vote_id', 'title', 'item1', 'item2', 'item3', 'is_done', 'start_date', 'done_date', 'vote_post', 'vote_line', 'vote_postsec', 'vote_user']

class VotePerSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    class Meta:
        model = VotePer
        fields = ['voteper_id', 'age', 'select', 'voteper_vote', 'voteper_user']



# --------------진행중 투표-------------------
class IngVoteSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    is_my=serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields=['vote_id','title','vote_user','item1', 'item2', 'item3', 'is_my']
    def get_is_my(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.vote_user == request.user
        return False

class IngVoteLineSerializer(serializers.ModelSerializer):
    IngVote=IngVoteSerializer(source='vote_line',many=True)
    class Meta:
        model = Line
        fields=['line_id','content','IngVote']
    def to_representation(self, instance):  
        request = self.context.get('request')   
        representation = super().to_representation(instance)

        queryset = Vote.objects.filter(vote_line=instance.line_id,is_done=False)
        serializer = IngVoteSerializer(queryset, many=True, context={'request': request}) 
        representation['IngVote'] = serializer.data

        return representation

# --------------완료된 투표-------------------


class DoneVoteSerializer(serializers.ModelSerializer):
    vote_user=UserProfileSerializer()
    result=serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields=['vote_id','title','item1', 'item2', 'item3','start_date','done_date', 'vote_user','result']
    def get_result(self, instance):
        result = {}  # 결과를 저장할 딕셔너리
        for age, _ in VotePer.AGES:
            for select, _ in VotePer.SELECTS:
                result[f"result{select}_{age}"] = VotePer.objects.filter(voteper_vote=instance, age=age, select=select).count()
        return result

class DoneVoteLineSerializer(serializers.ModelSerializer):
    DoneVote=DoneVoteSerializer(source='vote_line',many=True)
    class Meta:
        model = Line
        fields=['line_id','content','DoneVote']
    def to_representation(self, instance):  
        request = self.context.get('request')   
        representation = super().to_representation(instance)

        queryset = Vote.objects.filter(vote_line=instance.line_id,is_done=True)
        serializer = DoneVoteSerializer(queryset, many=True, context={'request': request}) 
        representation['DoneVote'] = serializer.data

        return representation

# --------------내가 만든 투표-------------------

class MyVoteLineSerializer(serializers.ModelSerializer):
    IngVote=IngVoteSerializer(source='vote_line',many=True)
    DoneVote=DoneVoteSerializer(source='vote_line',many=True)
    class Meta:
        model = Line
        fields=['line_id','content','IngVote','DoneVote']
    def to_representation(self, instance):  
        request = self.context.get('request')   
        representation = super().to_representation(instance)

        queryset1 = Vote.objects.filter(vote_line=instance.line_id,is_done=False)
        serializer1 = IngVoteSerializer(queryset1, many=True, context={'request': request}) 
        representation['IngVote'] = serializer1.data

        queryset2 = Vote.objects.filter(vote_line=instance.line_id,is_done=True)
        serializer2 = DoneVoteSerializer(queryset2, many=True, context={'request': request}) 
        representation['DoneVote'] = serializer2.data

        return representation

