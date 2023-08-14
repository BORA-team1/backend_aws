from django.db import models
from account.models import User
from post.models import PostSec
from line.models import Line

# Create your models here.
class Debate(models.Model):
    CONDS=((1,'모집중'),(2,'진행중'),(3,'완료'))
    debate_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=400)
    num=models.IntegerField()
    cond=models.IntegerField(choices=CONDS)
    debate_user=models.ForeignKey(User, related_name='debate_user',on_delete=models.SET_NULL,null=True)
    debate_postsec=models.ForeignKey(PostSec, related_name='debate_postsec',on_delete=models.CASCADE)
    debate_line=models.ForeignKey(Line, related_name='debate_line',on_delete=models.CASCADE)
    debaters=models.ManyToManyField(User, related_name='debaters')
    pros=models.ManyToManyField(User, related_name='pros')
    cons=models.ManyToManyField(User, related_name='cons')