from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadFrequency = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class InvitationCode(models.Model):
    invitationCode=models.CharField(max_length=10, unique=True,null=False)
    email=models.EmailField()
    def __str__(self):
        return self.invitationCode