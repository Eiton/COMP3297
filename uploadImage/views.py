from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uploadImage.forms import ImageForm
from uploadImage.models import Image
from uploadImage.models import Member
from uploadImage.models import Tag
from uploadImage.models import Image_tag
import datetime

# Create your views here.
def index(request):
    return render(request,'uploadPage.html',{})

def upload_file(request):
    if request.method == 'POST':
            newImg = Image()
            newImg.title = request.POST.get("title",'error')
            newImg.description = request.POST.get("description",'')
            newImg.category = request.POST.get("category",'')
            newImg.imageFile = request.FILES['image']
            newImg.time = datetime.datetime.now()
            newImg.numberOfView = 0
            newImg.likes = 0
            temp=Member.objects.filter(username='Dave')
            newImg.author=temp[0]
            newImg.save()
            tag=Tag.objects.filter(name=request.POST.get("tag",'none'))
            if not tag:
                tag = Tag()
                tag.name=request.POST.get("tag",'none')
                tag.save()
            else:
                tag=tag[0]
            image_tag=Image_tag()
            image_tag.image=newImg
            image_tag.tag=tag
            image_tag.save()
            return HttpResponse("<img src='"+newImg.imageFile.url+"'>")
    return HttpResponse("fail")