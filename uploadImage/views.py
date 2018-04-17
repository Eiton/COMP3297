from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uploadImage.models import Image,Tag
from mainPage.models import MemberInfo
from django.contrib.auth.models import User
import datetime

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 3
MAXIMUM_UPLOAD_FREQUENCY = 2
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../">back</a>')
    return render(request,'uploadPage.html')

def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    if request.method == 'POST':
            imgAuthor=request.user
            authorInfo=MemberInfo.objects.get(user=imgAuthor)
            numImage=len(Image.objects.filter(author=imgAuthor))
            newImg = Image()
            newImg.title = request.POST.get("title",'')
            if request.POST["title"]=='':
                return HttpResponse("Upload failed: Please specify a title<br><a href='./'>back to upload page</a>")
            newImg.description = request.POST.get("description",'')
            if request.POST["description"]=='':
                return HttpResponse("Upload failed: Please specify the description<br><a href='./'>back to upload page</a>")
            newImg.category = request.POST.get("category",'')
            if request.POST["tag"]=='':
                return HttpResponse("Upload failed: Please specify a tag<br><a href='./'>back to upload page</a>")
            if request.POST.get("image",'none')=='':
                return HttpResponse("Upload failed: no image is selected<br><a href='./'>back to upload page</a>")
            newImg.imageFile = request.FILES['image']
            newImg.time = datetime.datetime.now()
            newImg.numberOfView = 0
            newImg.numberOfDownload = 0
            newImg.likes = 0
            newImg.author=imgAuthor
            if numImage>=TOTAL_NUMBER_OF_AVAILABLE_IMAGE:
                return HttpResponse("Upload failed: Number of images uploaded exceeds the limit.<br> <a href='./'>back to upload page</a>")
            if authorInfo.uploadFrequency>=MAXIMUM_UPLOAD_FREQUENCY:
                return HttpResponse("Upload failed: Number of images uploaded exceeds the daily limit.<br> <a href='./'>back to upload page</a>")
            tag=Tag.objects.filter(name=request.POST.get("tag",'none'))
            if not tag:
                tag = Tag()
                tag.name=request.POST.get("tag",'none')
                tag.save()
            else:
                tag=tag[0]
            newImg.save()
            newImg.tags.add(tag)
            newImg.save()
            authorInfo.uploadFrequency+=1
            authorInfo.save()
            return HttpResponse("The image is uploaded successfully. <br><img src='"+newImg.imageFile.url+"'><br> <a href='./'>back to upload page</a>")
    return HttpResponse("Upload failed<br> <a href='./'>back to upload page</a>")
def download(request, pk):
    img=Image.objects.get(id=pk)
    img.numberOfDownload+=1
    img.save()
    return HttpResponse("<script>window.close()</script>")