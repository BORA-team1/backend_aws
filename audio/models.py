from django.db import models
from post.models import Post
from account.models import Hashtag, User

# Create your models here.

class Audio(models.Model):
    audio_id=models.AutoField(primary_key=True)
    long=models.IntegerField()
    audio_post=models.ForeignKey(Post,related_name='audio_post',on_delete=models.CASCADE)
    audiofile=models.TextField( null=True, blank=True)

    def __str__(self):
        return "{}: {}({})의 오디오".format(self.audio_id,self.audio_post.title,self.audio_post.post_id)

# class AudioSec(models.Model):
#     audiosec_id=models.AutoField(primary_key=True)
#     num=models.IntegerField()
#     audiofile=models.TextField( null=True, blank=True)
#     audiosec_audio=models.ForeignKey(Audio,related_name='audiosec_audio',on_delete=models.CASCADE)

class Playlist(models.Model):
    playlist_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    des=models.CharField(max_length=400,null=True,blank=True)
    is_base=models.BooleanField(default=False)
    first_audio=models.ForeignKey(Audio,related_name='first_audio',on_delete=models.SET_NULL,null=True)
    playlist_audio=models.ManyToManyField(Audio,related_name='playlist_audio')
    hashtag=models.ManyToManyField(Hashtag)
    mypli_user=models.ForeignKey(User, related_name='mypli_user',on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.playlist_id,self.title)