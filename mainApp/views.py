from django.shortcuts import render
from .models import Invitation,MemberInfo,Token, Image,Tag
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db.models import Count
import logging
import datetime

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 3
MAXIMUM_UPLOAD_FREQUENCY = 4
MAXIMUM_NUMBER_OF_TAGS = 10


def index(request):
    keywords=request.GET.get("keyword",'').split()
    if len(keywords):
        tags=Tag.objects.filter(name__in=keywords)
        images=Image.objects.filter(tags__in=tags).annotate(count=Count('id'))
    else:
        images=Image.objects.all().annotate(count=Count('id'))
    if request.GET.get("category",'') != '':
        images=images.filter(category=request.GET.get("category",''))
    if request.GET.get("photographer",'') !='':
        photographer = MemberInfo.objects.filter(displayname=request.GET.get("photographer",''))
        member = User.objects.filter(memberInfo__in=photographer)
        images=images.filter(author__in=member)
    if len(images)==0:
        return render(request,'mainPage.html',{'images':  '', 'user':request.user})
    if request.GET.get("order",'')=='time':
        images_ = images.order_by('count','time','popularity').reverse()
    else:
        images_= images.order_by('count','popularity','time').reverse()
    images = []
    for image in images_:
        if image.author==request.user or not request.user.is_authenticated:
            images.append([image,0])
        elif len(image.likes.filter(pk=request.user.pk))>0:
            images.append([image,1])
        else:
            images.append([image,2])
    return render(request,'mainPage.html',{'images': images,'user':request.user})

def profile(request,username):
    if request.method == 'POST':
        request.user.memberInfo.displayname=request.POST.get("displayname",'')
        request.user.memberInfo.selfDescription=request.POST.get("selfDescription",'')
        request.user.memberInfo.save()
        request.user.email=request.POST.get("contactAddress",'')
        request.user.save()
        return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'The profile information is changed successfully'})
    member = User.objects.get(username=username)
    images=Image.objects.filter(author=member).order_by('time').reverse()
    if len(images)==0:
        return render(request,'profile.html',{'user':request.user,'member': member,'images':""})
    ret=[]
    for image in images:
        if image.author==request.user or not request.user.is_authenticated:
            ret.append([image,0])
        elif len(image.likes.filter(pk=request.user.pk))>0:
            ret.append([image,1])
        else:
            ret.append([image,2])
    return render(request,'profile.html',{'user':request.user,'member': member,'images':ret})

def invite(request):
    if not request.user.is_authenticated:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please login first!'})
    if request.method == 'POST':
        emailAddress=request.POST.get("email",'')
        if emailAddress == '':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please specify the email address!'})
        else:
            randomInvitationCode = get_random_string(length=10)
            while len(Invitation.objects.filter(invitationCode=randomInvitationCode))>0:
                randomInvitationCode = get_random_string(length=10)
            newInvitation=Invitation();
            newInvitation.invitationCode=randomInvitationCode
            newInvitation.email=emailAddress
            newInvitation.save()
            logger = logging.getLogger('invitationMail')
            emailMessage="To: "+emailAddress+"\n"+"Dear photographer,\n"+"Go to http://localhost:8000/, fill in the invitation code "+randomInvitationCode+" and become a member of imageX!\n"+"imageX team" 
            logger.info(emailMessage)
            return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'An invitation email will be sent to '+emailAddress+'.'})
    return render(request,'invite.html')

def register(request):
    if request.method == 'POST':
        invitation=Invitation.objects.filter(invitationCode=request.POST.get("invitationCode",''))
        if len(invitation)==0:
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Invalid invitation code!'})
        userName=request.POST.get("username",'')
        if userName=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please enter a username!'})
            
        if len(User.objects.filter(username=userName))>0:
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Username already exists!'})
        pwd=request.POST.get("password",'')
        if pwd=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please enter a password!'})
        user = User.objects.create_user(userName, invitation[0].email, pwd)
        member=MemberInfo()
        member.user=user
        member.displayname=userName
        member.selfDescription=""
        member.save()
        invitation[0].delete()
        return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'Registered successfully, welcome to imageX!','jump':'main'})
    return render(request,'register.html')

def forgotPassword(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(username=request.POST.get("username",''))
        except User.DoesNotExist:
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Username does not exist!'})
        emailAddress=user.email
        randomToken = get_random_string(length=10)
        while len(Token.objects.filter(token=randomToken))>0:
            randomToken = get_random_string(length=10)
        token=Token()
        token.user=user
        token.token=randomToken
        token.save()
        logger = logging.getLogger('invitationMail')
        emailMessage="To: "+emailAddress+"\n"+"Dear photographer,\n"+"Enter the token "+randomToken+" to reset your password.\n"+"imageX team" 
        logger.info(emailMessage)
        return redirect(resetPassword)
    return render(request,'forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        try:
            token=Token.objects.get(token=request.POST.get("token",''))
        except Token.DoesNotExist:
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Incorrect token!'})
        if request.POST.get("password",'')=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please enter the new password!'})
        if request.POST.get("password2",'')=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please repeat the new password!'})
        if request.POST.get("password",'')!=request.POST.get("password2",''):
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'The two passwords are not the same!'})
        token.user.set_password(request.POST.get("password",''))
        token.user.save()
        token.delete()
        return HttpResponse("reset successfully<br>"+"""
        <script>
            function redir()
            {
                window.location='../';
            }
            setTimeout('redir()',1500);
         </script>""")
    return render(request,'resetPassword.html')
    
def changePassword(request):
    if not request.user.is_authenticated:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please login first'})
    if request.method == 'POST':
        if request.POST.get("currentPassword",'')=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please enter the current password!'})
        if request.POST.get("newPassword",'')=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please enter the new password!'})
        if request.POST.get("newPassword2",'')=='':
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please repeat the new password!'})
        if not request.user.check_password(request.POST.get("currentPassword",'')):
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Incorrect password!'})
        if request.POST.get("newPassword",'')!=request.POST.get("newPassword2",''):
            return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'The two new passwords are not the same!'})
        request.user.set_password(request.POST.get("newPassword",''))
        request.user.save()
        return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'The password is changed successfully, please login again','jump':'main'})
    return render(request,'changePassword.html')
    
def uploadPage(request):
    if not request.user.is_authenticated:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please login first'})
    if request.method == 'POST':
        return uploadImage(request)
    numImage=len(Image.objects.filter(author=request.user))
    if numImage>=TOTAL_NUMBER_OF_AVAILABLE_IMAGE:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Number of images uploaded exceeds the limit.'})
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    numImageToday=len(Image.objects.filter(author=request.user, time__range=(today_min, today_max)))
    if numImageToday>=MAXIMUM_UPLOAD_FREQUENCY:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Number of images uploaded exceeds the daily limit.'})
    return render(request,'uploadPage.html')
    
def uploadImage(request):
    if not request.user.is_authenticated:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please login first'})
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
                return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'no image is selected'})
            imgTags=request.POST.get("tags",'').split()
            if len(imgTags)>MAXIMUM_NUMBER_OF_TAGS:
                return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'number of tags per image is limited to 10'})
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
            return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'The image is uploaded successfully.','jump':'main'})
    return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Upload failed'})
    
def delete(request, pk):
    if not request.user.is_authenticated:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'Please login first'})
    try: 
        img=Image.objects.get(id=pk)
    except Image.DoesNotExist:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'image does not exist!'})
    if img.author!=request.user:
        return render(request,'messagePage.html',{'user':request.user,'title':'Error','message':'You are not the uploader of the image!'})
    img.delete()
    return render(request,'messagePage.html',{'user':request.user,'title':'Success','message':'Image is deleted successfully.'})

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