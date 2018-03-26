from django.shortcuts import render
from uploadImage.models import Image,Tag
# Create your views here.
def index(request):
    keyword=request.GET.get("keyword",'')
    if keyword != '':
        tag=Tag.objects.filter(name=keyword)
        if len(tag)==0:
            return render(request,'mainPage.html',{'images':  ''})
        images=tag[0].image_set.all()
    else:
        images=Image.objects.all()
    return render(request,'mainPage.html',{'images': images})