from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='memberInfo')
    uploadFrequency = models.IntegerField(default=0)
    displayname = models.CharField(max_length=30, default="")
    selfDescription = models.CharField(max_length=300, default="",blank=True)
    def __str__(self):
        return self.displayname

class Invitation(models.Model):
    invitationCode=models.CharField(max_length=10, unique=True,null=False)
    email=models.EmailField()
    def __str__(self):
        return self.invitationCode
        
class Token(models.Model):
    token=models.CharField(max_length=10, unique=True,null=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Image(models.Model):
    title = models.CharField(max_length=30,blank=True)
    description = models.CharField(max_length=200,blank=True)
    time = models.DateTimeField()
    category = models.CharField(max_length=30,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    numberOfDownload=models.IntegerField(default=0)
    likes = models.ManyToManyField(User)
    popularity = models.IntegerField(default=0)
    imageFile = models.ImageField(upload_to='images/')
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title