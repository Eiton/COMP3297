from django.contrib import admin

# Register your models here.
from .models import Tag
from .models import Image
from .models import Category
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Category)