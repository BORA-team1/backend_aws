from django.db import models
from post.models import Post, PostSec
from account.models import User

# Create your models here.

class Line(models.Model):
    line_id=models.AutoField(primary_key=True)
    sentence=models.IntegerField()
    content=models.TextField()
    line_post=models.ForeignKey(Post, related_name='line_post',on_delete=models.CASCADE)
    line_postsec=models.ForeignKey(PostSec, related_name='line_postsec',on_delete=models.CASCADE)
    line_user=models.ManyToManyField(User, related_name='line_user')

    def __str__(self):
        return "{}: '{}'의 {}번째 섹션의 {}번째문장".format(self.line_id,self.line_post.title,self.line_postsec.num,self.sentence)

class LineCom(models.Model):
    linecom_id=models.AutoField(primary_key=True)
    content=models.TextField()
    linecom_line=models.ForeignKey(Line, related_name='linecom_line',on_delete=models.CASCADE)
    linecom_postsec=models.ForeignKey(PostSec, related_name='linecom_postsec',on_delete=models.CASCADE)
    linecom_user=models.ForeignKey(User, related_name='linecom_user',on_delete=models.CASCADE)
    like=models.ManyToManyField(User,related_name='linecom_like')

    def __str__(self):
        return "{}: '{}'의 밑줄 {}의 댓글".format(self.linecom_id,self.linecom_line.line_post.title,self.linecom_line.line_id)

class LineComCom(models.Model):
    linecomcom_id=models.AutoField(primary_key=True)
    content=models.TextField()
    linecomcom_lineCom=models.ForeignKey(LineCom, related_name='linecomcom_lineCom',on_delete=models.CASCADE)
    linecomcom_user=models.ForeignKey(User, related_name='linecomcom_user',on_delete=models.CASCADE)
    mention=models.CharField(max_length=40,null=True)

    def __str__(self):
        return "{}: '{}'의 밑줄 {}의 댓글 {}의 답글".format(self.linecomcom_id,self.linecomcom_lineCom.linecom_line.line_post.title,self.linecomcom_lineCom.linecom_line.line_id,self.linecomcom_lineCom.linecom_id)

class Question(models.Model):
    que_id=models.AutoField(primary_key=True)
    content=models.TextField()
    # num=models.IntegerField(null=True,blank=True,default=0)
    que_line=models.ForeignKey(Line, related_name='que_line',on_delete=models.CASCADE)
    que_postsec=models.ForeignKey(PostSec, related_name='que_postsec',on_delete=models.CASCADE)
    que_user=models.ForeignKey(User, related_name='que_user',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return "{}: '{}'의 밑줄 {}의 질문".format(self.que_id,self.que_line.line_post.title,self.que_line.line_id)


class Answer(models.Model):
    ans_id=models.AutoField(primary_key=True)
    content=models.TextField()
    ans_que=models.ForeignKey(Question, related_name='ans_que',on_delete=models.CASCADE)
    ans_user=models.ForeignKey(User, related_name='ans_user',on_delete=models.CASCADE)

    def __str__(self):
        return "{}: '{}'의 밑줄 {}의 질문({})".format(self.ans_id,self.ans_que.que_line.line_post.title,self.ans_que.que_line.line_id,self.ans_que.content)

class Emotion(models.Model):
    EMOS = (       # json형태 보고 Choice말고 그냥 Int로 해야할수도..
        (1, 'happy'),
        (2, 'surprise'),
        (3, 'angry'),
        (4, 'sad'),
        (5, 'serious')
    )
    emo_id=models.AutoField(primary_key=True)
    content=models.IntegerField(choices=EMOS)
    emo_line=models.ForeignKey(Line, related_name='emo_line',on_delete=models.CASCADE)
    emo_postsec=models.ForeignKey(PostSec, related_name='emo_postsec',on_delete=models.CASCADE)
    emo_user=models.ForeignKey(User, related_name='emo_user',on_delete=models.CASCADE)

    def __str__(self):
        return "{}: '{}'의 밑줄 {}의 표정({})".format(self.emo_id,self.emo_line.line_post.title,self.emo_line.line_id,self.content)

