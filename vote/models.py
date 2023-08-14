from django.db import models
from post.models import Post, PostSec
from line.models import Line
from account.models import User

# Create your models here.
class Vote (models.Model):
    vote_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=400)
    item1=models.CharField(max_length=400)
    item2=models.CharField(max_length=400)
    item3=models.CharField(max_length=400)
    is_done=models.BooleanField(default=False)                                  # 기본값 False 
    start_date=models.DateField(auto_now_add=True)                          # 생성된 날짜로 저장
    done_date=models.DateField(null=True, default=None)                     
    vote_post=models.ForeignKey(Post, related_name='vote_post',on_delete=models.CASCADE)
    vote_line=models.ForeignKey(Line, related_name='vote_line',on_delete=models.CASCADE)
    vote_postsec=models.ForeignKey(PostSec, related_name='vote_postsec',on_delete=models.CASCADE)
    vote_user=models.ForeignKey(User, related_name='vote_user',on_delete=models.SET_NULL,null=True)            # 투표 작성자

    def __str__(self):
        return "{}: {} - {}의 투표".format(self.vote_id,self.title,self.vote_line.line_post.title)

class VotePer(models.Model):
    AGES = (
        (1, '10대'),
        (2, '20대'),
        (3, '30대'),
        (4, '40대'),
        (5, '50대 이상')
    )
    SELECTS=(
        (1,1),
        (2,2),
        (3,3)
    )
    voteper_id=models.AutoField(primary_key=True)
    age=models.IntegerField(choices=AGES,null=True)
    select=models.IntegerField(choices=SELECTS,null=True)
    voteper_vote=models.ForeignKey(Vote, related_name='voteper_vote',on_delete=models.CASCADE)
    voteper_user=models.ForeignKey(User, related_name='voteper_user',on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}의 투표 - {}".format(self.voteper_id,self.voteper_vote.title,self.select)
