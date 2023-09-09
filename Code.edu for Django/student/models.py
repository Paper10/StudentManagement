import time
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=15, default="새로운 그룹")
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    group_pic = models.ImageField(
        default="default_profile_pic.jpg", upload_to="profile_pics"
    )
    
    def __str__(self):
        return self.group_name

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        default="새로운 닉네임" + str(time.time()),
        error_messages={"unique": "이미 사용중인 닉네임입니다."},
    )
    profile_pic = models.ImageField(
        default="default_profile_pic.jpg", upload_to="profile_pics"
    )
    intro = models.CharField(max_length=60, blank=True)
    teacher = models.BooleanField(default=False)
    group_in = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)



class Membership(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Question(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    viewer = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    image1 = models.ImageField(upload_to="question_pics", default="default_image_pic.jpg")
    image2 = models.ImageField(upload_to="question_pics", blank=True)
    image3 = models.ImageField(upload_to="question_pics", blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Problem(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        unique_together = ('group', 'number')
        ordering = ['number']

    def __str__(self):
        return f'{self.group} Class : {self.number}'
