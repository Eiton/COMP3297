from django.contrib import admin


from .models import Invitation
from .models import MemberInfo
from .models import Token
from .models import Tag
from .models import Image
admin.site.register(Invitation)
admin.site.register(MemberInfo)
admin.site.register(Token)
admin.site.register(Tag)
admin.site.register(Image)