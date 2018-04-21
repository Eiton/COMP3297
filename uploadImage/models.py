from django.db import models
from django.contrib.auth.models import User
# Create your models here.
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