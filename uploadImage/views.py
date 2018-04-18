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
categorys = [('Abstract','1'),('Aerial','2'),('Animals','3'),('Architecture','4'),
             ('Black and White','5'),('Family','6'),('Fashion','7'),('Fine Art','8'),
             ('Food','9'),('Journalism','10'),('Landscape','11'),('Macro','12'),('Nature','13'),
             ('Night','14'),('People','15'),('Performing Arts','16'),('Sport','17'),
             ('Still Life','18'),('Street','19'),('Travel','20')]
def index(request):
    pretags.clear()
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../">back</a>')
    return render(request,'uploadPage.html',{'category_':categorys})
    
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('error:please login first<br><a href="../../">back</a>')
    
    title=request.POST.get("title",'')
    description=request.POST.get("description",'')
    id_=request.POST.get('category')
    categorys_=list(categorys)
    for category,id in categorys:
        if id_ == id:
          categorys_.remove((category,id))
          categorys_.insert(0,(category,id_))
          break
    if request.POST.get("Add"):
        if len(pretags) < 10:
            pretag=request.POST.get("tag")
            if pretag =='':
              return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'You do not type anything!','category_':categorys_,'title':title,'description':description})
            pretags.append(pretag);
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'','category_':categorys_,'title':title,'description':description})
        else:
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'You reach the maxiumum numbers of tags.','category_':categorys_,'title':title,'description':description})
    
    for pretag in pretags:
        if request.POST.get(pretag):
            pretags.remove(pretag);
            return render(request,'uploadPage.html',{'pretags': pretags,'errormsg':'','category_':categorys_,'title':title,'description':description})
            
    if request.method == 'POST':
            imgAuthor=request.user
            try:
                authorInfo=MemberInfo.objects.get(user=imgAuthor)
            except MemberInfo.DoesNotExist:
                authorInfo=MemberInfo()
                authorInfo.user=request.user
                authorInfo.uploadFrequency=0
                authorInfo.save()
            numImage=len(Image.objects.filter(author=imgAuthor))
            newImg = Image()
            newImg.title = request.POST.get("title",'')
            if request.POST["title"]=='':
                return HttpResponse("Upload failed: Please specify a title<br><a href='./'>back to upload page</a>")
            newImg.description = request.POST.get("description",'')
            if request.POST["description"]=='':
                return HttpResponse("Upload failed: Please specify the description<br><a href='./'>back to upload page</a>")
            for category,id in categorys:
                if id_==id:
                  category_=category
            newImg.category=Category.objects.get(name=category_)
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