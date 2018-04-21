from django.shortcuts import render
from uploadImage.models import Image,Tag
from mainPage.models import InvitationCode,MemberInfo,Token
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.db.models import Count
import logging

TOTAL_NUMBER_OF_AVAILABLE_IMAGE = 10
MAXIMUM_UPLOAD_FREQUENCY = 10
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
        try:
            photographer = User.objects.get(username=request.GET.get("photographer",''))
            images=images.filter(author=photographer)
        except User.DoesNotExist:
            images=[]
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
    member = User.objects.get(username=username)
    images=Image.objects.filter(author=member)
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
        return HttpResponse('error:please login first<br><a href="../">back</a>')
    if request.method == 'POST':
        emailAddress=request.POST.get("email",'')
        if emailAddress != '':
            randomInvitationCode = get_random_string(length=10)
            while len(InvitationCode.objects.filter(invitationCode=randomInvitationCode))>0:
                randomInvitationCode = get_random_string(length=10)
            newInvitationCode=InvitationCode();
            newInvitationCode.invitationCode=randomInvitationCode
            newInvitationCode.email=emailAddress
            newInvitationCode.save()
            logger = logging.getLogger('invitationMail')
            emailMessage="To: "+emailAddress+"\n"+"Dear photographer,\n"+"Go to http://localhost:8000/, fill in the invitation code "+randomInvitationCode+" and become a member of imageX!\n"+"imageX team" 
            logger.info(emailMessage)
            return HttpResponse("An invitation email will be sent to "+emailAddress+".<br><a href=''>Back</a>")
        else:
            return HttpResponse("error: Please specify the email address!<br><a href=''>Back</a>")
    return render(request,'invite.html')

def register(request):
    if request.method == 'POST':
        if len(InvitationCode.objects.filter(invitationCode=request.POST.get("invitationCode",'')))==0:
            return HttpResponse("error: Invalid invitation code!<br><a href=''>Back</a>")
        invitation=InvitationCode.objects.get(invitationCode=request.POST.get("invitationCode",''))
        userName=request.POST.get("username",'')
        if userName=='':
            return HttpResponse("error: Please enter a username!<br><a href=''>Back</a>")
        if len(User.objects.filter(username=userName))>0:
            return HttpResponse("error: Username already exists!<br><a href=''>Back</a>")
        pwd=request.POST.get("password",'')
        if pwd=='':
            return HttpResponse("error: Please enter a password!<br><a href=''>Back</a>")
        user = User.objects.create_user(userName, invitation.email, pwd)
        member=MemberInfo()
        member.user=user
        member.displayname=userName
        member.selfDescription=""
        member.save()
        invitation.delete()
        return HttpResponse("registered successfully, welcome to imageX!<br><a href='../'>back to main page</a>")
    return render(request,'register.html')

def forgotPassword(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(username=request.POST.get("username",''))
        except User.DoesNotExist:
            return HttpResponse("error:username does not exist!<br><a href=''>back</a>")
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
            return HttpResponse("error:incorrect token!<br><a href=''>back</a>")
        if request.POST.get("password",'')=='':
            return HttpResponse("error:Please enter the new password!<br><a href=''>back</a>")
        if request.POST.get("password2",'')=='':
            return HttpResponse("error:Please repeat the new password!<br><a href=''>back</a>")
        if request.POST.get("password",'')!=request.POST.get("password2",''):
            return HttpResponse("error:the two password are not the same!<br><a href=''>back</a>")
        token.user.set_password(request.POST.get("password",''))
        token.user.save()
        token.delete()
        return HttpResponse("reset successfully<br><a href='../'>back to main page</a>")
    return render(request,'resetPassword.html')
    
def changePassword(request):
    if request.method == 'POST':
        if request.POST.get("currentPassword",'')=='':
            return HttpResponse("error:Please enter the current password!<br><a href=''>back</a>")
        if request.POST.get("newPassword",'')=='':
            return HttpResponse("error:Please enter the new password!<br><a href=''>back</a>")
        if request.POST.get("newPassword2",'')=='':
            return HttpResponse("error:Please repeat the new password!<br><a href=''>back</a>")
        if not request.user.check_password(request.POST.get("currentPassword",'')):
            return HttpResponse("error:incorrect password!<br><a href=''>back</a>")
        if request.POST.get("newPassword",'')!=request.POST.get("newPassword2",''):
            return HttpResponse("error:the two new password are not the same!<br><a href=''>back</a>")
        request.user.set_password(request.POST.get("newPassword",''))
        request.user.save()
        return HttpResponse("reset successfully<br><a href='../'>back to main page</a>")
    return render(request,'changePassword.html')
    