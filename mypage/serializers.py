from rest_framework import serializers
from .models import *
from collections import OrderedDict
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import UserProfileSerializer,InterestSerializer
from account.models import User
from post.models import Post
from audio.models import Playlist,Audio

# class FollowsSerializer(serializers.ModelSerializer):
#     follow=UserProfileSerializer(many=True, read_only=True)
#     class Meta:
#         model=User
#         fields=['follow']

class MyPageSerializer(serializers.ModelSerializer):
    interest=InterestSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields=['id','profile','nickname','interest']

class BookPostSerializer(serializers.ModelSerializer):
    hashtag=InterestSerializer(many=True, read_only=True)
    is_booked = serializers.BooleanField(default=False)
    class Meta:
        model=Post
        fields=['post_id','title','post_image','diff','is_booked','hashtag']

class MyPliSerializer(serializers.ModelSerializer):
    img=serializers.SerializerMethodField()
    class Meta:
        model=Playlist
        fields=['playlist_id','title','des','first_audio','img']
    
    def get_img(self, playlist):
        audio_posts = playlist.playlist_audio.all()[:4].values_list('audio_post__post_image', flat=True)
        return list(audio_posts)
