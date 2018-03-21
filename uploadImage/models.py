from django.db import models

# Create your models here.
class Member(models.Model):
    username = models.CharField(max_length=30)
    def __str__(self):
        return self.username
class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
class Image(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    time = models.DateTimeField()
    category = models.CharField(max_length=30)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    numberOfView= models.IntegerField()
    likes= models.IntegerField()
    imageFile = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.title
class Image_tag(models.Model):
    image=models.ForeignKey(Image, on_delete=models.CASCADE)
    tag=models.ForeignKey(Tag, on_delete=models.CASCADE)
    def __str__(self):
        return self.image
    
