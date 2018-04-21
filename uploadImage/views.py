from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uploadImage.models import Image,Tag
from mainPage.models import MemberInfo
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import json
import datetime

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 10
MAXIMUM_UPLOAD_FREQUENCY = 10
MAXIMUM_NUMBER_OF_TAGS = 10
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../">back</a>')
    numImage=len(Image.objects.filter(author=request.user))
    if numImage>=TOTAL_NUMBER_OF_AVAILABLE_IMAGE:
        return HttpResponse("error:Number of images uploaded exceeds the limit.<br> <a href='./'>back</a>")
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    numImageToday=len(Image.objects.filter(author=request.user, time__range=(today_min, today_max)))
    if numImageToday>=MAXIMUM_UPLOAD_FREQUENCY:
        return HttpResponse("error:Number of images uploaded exceeds the daily limit.<br> <a href='./'>back</a>")
    return render(request,'uploadPage.html')
    
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    if request.method == 'POST':
            imgAuthor=request.user
            try:
                authorInfo=MemberInfo.objects.get(user=imgAuthor)
            except MemberInfo.DoesNotExist:
                authorInfo=MemberInfo()
                authorInfo.user=request.user
                authorInfo.uploadFrequency=0
                authorInfo.save()
            newImg = Image()
            newImg.title = request.POST.get("title",'')
            newImg.description = request.POST.get("description",'')
            newImg.category=request.POST.get("category",'')
            if request.POST.get("image",'none')=='':
                return HttpResponse("Upload failed: no image is selected<br><a href='./'>back to upload page</a>")
            imgTags=request.POST.get("tags",'').split()
            if len(imgTags)>MAXIMUM_NUMBER_OF_TAGS:
                return HttpResponse("Upload failed:  the number of tags per image is limited to 10<br><a href='./'>back to upload page</a>")
            newImg.imageFile = request.FILES['image']
            newImg.time = datetime.datetime.now()
            newImg.numberOfView = 0
            newImg.numberOfDownload = 0
            newImg.author=imgAuthor
            newImg.save()
            for imgTag in imgTags:
                tag=Tag.objects.filter(name=imgTag)
                if not tag:
                    tag = Tag()
                    tag.name=imgTag
                    tag.save()
                    newImg.tags.add(tag)
                else:
                    newImg.tags.add(tag[0])
            newImg.save()
            return HttpResponse("The image is uploaded successfully. <br><img src='"+newImg.imageFile.url+"'><br> <a href='./'>back to upload page</a>")
    return HttpResponse("Upload failed<br> <a href='./'>back to upload page</a>")
    
def delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    try: 
        img=Image.objects.get(id=pk)
    except Image.DoesNotExist:
        return HttpResponse('error:image does not exist!<br><a href="../../">back</a>')
    if img.author!=request.user:
        return HttpResponse('error:You are not the uploader of the image!<br><a href="../../">back</a>')
    img.delete()
    return HttpResponse("""Image is deleted successfully.<br>
        <script>
            function back()
            {
                window.history.back();
            }
            setTimeout('back()',1500);
         </script>""")

def download(request, pk):
    image=Image.objects.get(id=pk)
    image.numberOfDownload+=1
    image.popularity+=1
    image.save()
    if image.author==request.user or not request.user.is_authenticated:
        status=0
    elif len(image.likes.filter(pk=request.user.pk))>0 :
        status=1
    else:
        status=2
    return render(request,'imageInfo.html',{'image': image, 'status':status})
         
def like(request, pk):
    member=request.user
    image=Image.objects.get(id=pk)
    if len(image.likes.filter(pk=request.user.pk))>0:
        image.likes.remove(member)
        image.popularity-=1
        status=2
    else:
        image.likes.add(member)
        image.popularity+=1
        status=1
    image.save()
    return render(request,'imageInfo.html',{'image': image, 'status':status})
    
def imageInfo(request, pk):
    image=Image.objects.get(id=pk)
    if image.author==request.user or not request.user.is_authenticated:
        status=0
    elif len(image.likes.filter(pk=request.user.pk))>0 :
        status=1
    else:
        status=2
    return render(request,'imageInfo.html',{'image': image, 'status':status})
    