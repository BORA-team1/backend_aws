from django.db import models
from account.models import User
from post.models import Post

# Create your models here.

class Han(models.Model):
    han_id=models.AutoField(primary_key=True)
    content=models.TextField()
    han_user=models.ForeignKey(User, related_name='han_user',on_delete=models.SET_NULL,null=True)
    han_post=models.ForeignKey(Post, related_name='han_post',on_delete=models.CASCADE)
    like=models.ManyToManyField(User,related_name='han_like')

    def __str__(self):
        return "{}: {}의 한마디".format(self.han_id,self.han_post.title)


class HanCom(models.Model):
    hancom_id=models.AutoField(primary_key=True)
    content=models.TextField()
    hancom_han=models.ForeignKey(Han, related_name='hancom_han',on_delete=models.CASCADE)
    hancom_user=models.ForeignKey(User, related_name='hancom_user',on_delete=models.CASCADE)
    mention=models.CharField(max_length=40,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}의 답글, post: {}".format(self.hancom_id,self.hancom_han.han_id,self.hancom_han.han_post.title)