from django.contrib import admin

# Register your models here.
from .models import Member
from .models import Tag
from .models import Image
from .models import Image_tag
admin.site.register(Member)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Image_tag)