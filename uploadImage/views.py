from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uploadImage.models import Image
from uploadImage.models import Member
from uploadImage.models import Tag
from uploadImage.models import Image_tag
import datetime

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 3
MAXIMUM_UPLOAD_FREQUENCY = 4
# Create your views here.
def index(request):
    return render(request,'uploadPage.html',{'members': Member.objects.all()})

def upload_file(request):
    if request.method == 'POST':
            imgAuthor=Member.objects.get(username=request.POST.get("author",'none'))
            numImage=len(Image.objects.filter(author=imgAuthor))
            if numImage>=TOTAL_NUMBER_OF_AVAILABLE_IMAGE:
                return HttpResponse("Upload failed: Number of images uploaded exceeds the limit.<br> <a href='./'>back to upload page</a>")
            if imgAuthor.uploadFrequency>=MAXIMUM_UPLOAD_FREQUENCY:
                return HttpResponse("Upload failed: Number of images uploaded exceeds the daily limit.<br> <a href='./'>back to upload page</a>")
            imgAuthor.uploadFrequency+=1
            imgAuthor.save()
            newImg = Image()
            newImg.title = request.POST.get("title",'error')
            newImg.description = request.POST.get("description",'')
            newImg.category = request.POST.get("category",'')
            newImg.imageFile = request.FILES['image']
            newImg.time = datetime.datetime.now()
            newImg.numberOfView = 0
            newImg.likes = 0
            newImg.author=imgAuthor
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
            return HttpResponse("The image is uploaded successfully. <br><img src='"+newImg.imageFile.url+"'><br> <a href='./'>back to upload page</a>")
    return HttpResponse("Upload failed<br> <a href='./'>back to upload page</a>")