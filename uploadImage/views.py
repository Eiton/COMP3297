from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uploadImage.models import Image,Tag,Category
from mainPage.models import MemberInfo
from django.contrib.auth.models import User
import datetime

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 10
MAXIMUM_UPLOAD_FREQUENCY = 10
pretags=[]
categorys = ['Abstract','Aerial','Animals','Architecture','Black and White','Family',
             'Fashion','Fine Art','Food','Journalism','Landscape','Macro','Nature',
             'Night','People','Performing Arts','Sport','Still Life','Street','Travel']
             
def index(request):
    pretags.clear()
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../">back</a>')
    return render(request,'uploadPage.html')

def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    
    title=request.POST.get("title",'')
    description=request.POST.get("description",'')
    if request.POST.get("Add"):
        if len(pretags) < 10:
            pretag=request.POST.get("tag")
            if pretag =='':
              return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'You do not type anything!','title':title,'description':description})
            pretags.append(pretag);
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'','title':title,'description':description})
        else:
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'You reach the maxiumum numbers of tags.','title':title,'description':description})
    for pretag in pretags:
        if request.POST.get(pretag):
            pretags.remove(pretag);
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'','title':title,'description':description})
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
            newImg.category=Category.objects.get(name=request.POST.get("category",''))
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
            newImg.save()
            for pretag in pretags:
                tag=Tag.objects.filter(name=pretag)
                if not tag:
                    tag = Tag()
                    tag.name=pretag
                    tag.save()
                else:
                    tag=tag[0]
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
    
def delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    try: 
        img=Image.objects.get(id=pk)
    except Image.DoesNotExist:
        return HttpResponse('error:image does not exist!<br><a href="../../">back</a>')
    if img.author!=request.user:
        return HttpResponse('error:You are not the uploader of the image!<br><a href="../../">back</a>')
    if request.method != 'POST':
        return render(request,"deleteImage.html",{"image":img,"pk":pk})
    if request.POST["Confirm"]=="Yes":
        img.delete()
        return HttpResponse("""Image is deleted successfully.<br>
        <script>
            function back()
            {
                window.location.replace("../../profile");
            }
            setTimeout('back()',1500);
         </script>""")
    return HttpResponse("""Delection canceled.<br>
        <script>
            function back()
            {
                window.location.replace("../../profile");
            }
            setTimeout('back()',1500);
         </script>""")