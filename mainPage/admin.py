from django.contrib import admin

# Register your models here.
from .models import InvitationCode
from .models import MemberInfo
admin.site.register(InvitationCode)
admin.site.register(MemberInfo)