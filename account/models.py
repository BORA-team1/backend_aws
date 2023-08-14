from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Hashtag(models.Model):
    hashtag=models.CharField(max_length=100)

    def __str__(self):
        return self.hashtag
    
class User(AbstractUser):
    GENDERS = (
        ('남', '남'),
        ('여', '여'),
    )
    AGES = ( # json형태 보고 Choice말고 그냥 Int로 해야할수도..
        (1, '10대'),
        (2, '20대'),
        (3, '30대'),
        (4, '40대'),
        (5, '50대 이상')
    )
    # id=models.AutoField(primary_key=True)
    # username (아이디), password (패스워드) AbstractUser에 존재
    nickname=models.CharField(max_length=20)
    # profile=models.ImageField(upload_to = "user_profile", null=True, blank=True)
    profile=models.TextField( null=True, blank=True)
    # gender = models.CharField(choices=GENDERS, max_length=1,  default='여')
    is_publisher=models.BooleanField(default=False)
    age=models.IntegerField(choices=AGES,null=True)
    follow= models.ManyToManyField('self', symmetrical=False, related_name='follower')
    interest=models.ManyToManyField(Hashtag)
    
    def __str__(self):
        return "{}: {}".format(self.id,self.nickname)