from django.contrib import admin

# Register your models here.
from .models import Member
from .models import Tag
from .models import Image
admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Image)