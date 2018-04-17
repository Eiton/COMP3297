from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
		
class Category(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name        

class Image(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    time = models.DateTimeField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    numberOfView= models.IntegerField(default=0)
    numberOfDownload=models.IntegerField(default=0)
    likes= models.IntegerField(default=0)
    imageFile = models.ImageField(upload_to='images/')
    tags=models.ManyToManyField(Tag)
    def __str__(self):
        return self.title