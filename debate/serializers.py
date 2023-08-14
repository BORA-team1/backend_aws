from rest_framework import serializers
from django.shortcuts import render,get_object_or_404
from .models import *
from account.serializers import UserProfileSerializer


class DebateSerializer(serializers.ModelSerializer):
    debate_user=UserProfileSerializer()
    debaters=UserProfileSerializer(many=True)
    class Meta :
        model=Debate
        fields=['debate_id','title', 'num', 'cond', 'debate_user', 'debaters']

class LineIngDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,cond__lt=3).all()
        return DebateSerializer(debates, many=True).data
    
class LineDoneDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,cond=3).all()
        return DebateSerializer(debates, many=True).data
    
class LineMyDebateSerializer(serializers.ModelSerializer):
    Debate=serializers.SerializerMethodField()
    class Meta :
        model=Line
        fields=['line_id','content', 'Debate']
    def get_Debate(self, instance):
        request = self.context.get('request')
        line_id = instance.line_id
        debates = Debate.objects.filter(debate_line=line_id,debate_user=request.user.id).all()
        return DebateSerializer(debates, many=True).data
    
class NewDebateSerializer(serializers.ModelSerializer):
    class Meta :
        model=Debate
        fields=['debate_id','title', 'num','cond','debate_user','debate_postsec','debate_line']