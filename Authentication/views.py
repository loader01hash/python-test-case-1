from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Booking.models import UserDetails, AdminDetails,MovieDetails
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


def index(request):
#   template = loader.get_template('login.html')
#   return HttpResponse(template.render())
    return render(request,'login.html')



def check(user_name,user_password):
    user_list = [user.user_name for user in UserDetails.objects.all()]
    admin_list = [admin.admin_username for admin in AdminDetails.objects.all()]
    if user_name in admin_list:
        #if check_password(user_password, AdminDetails.objects.get(admin_username=user_name).admin_password):
        if AdminDetails.objects.get(admin_username=user_name).admin_password == user_password:
            return 1,True
        else:
            return 1,False
    elif user_name in user_list:
        #if check_password(user_password,UserDetails.objects.get(user_name=user_name).user_password):
        if UserDetails.objects.get(user_name=user_name).user_password == user_password:
            return 0,True
        else:
            return 0,False
    else:
        return None,False

def validate(request):
    user_name = request.POST['email']
    user_password = request.POST['password']
    entity, validity = check(user_name,user_password)
    
    if validity:
        if entity:
            #return HttpResponse('<h1>Admin Logged In ...</h1>')
            return redirect('Admindetails:index')
        else:
            #return render(request,'Authentication/homepage.html',{'movies':MovieDetails.objects.all()})
            return render (request, 'homepage.html',{'movies':MovieDetails.objects.all(), 'username':user_name})
    else:
        #return HttpResponse('<h1>Invalid Credentials !!</h1>')
        return render(request, 'invalid user.html')

def addnewuser(request):
    username = request.POST['name']
    password =  request.POST['password']
    #password =  make_password(request.POST['password'])
    age =  request.POST['age']
    number = request.POST['phone']
    # obj = UserDetails(user_name = username,user_password = password, user_age = age,user_phone_no = number )
    # obj.save()
    # return render(request, 'login.html')      
    if UserDetails.objects.filter(user_name = username).exists():
      messages.add_message(request, messages.ERROR, ' User Already Exits ! ') 
    else:
      obj = UserDetails(user_name = username,user_password = password, user_age = age,user_phone_no = number )
      obj.save()
      messages.add_message(request, messages.SUCCESS, ' Signup Successfully ')
    #return render(request,'login.html')
    return redirect('Authentication:index')


def viewprofile(request, username):
    #username = 'Manmeet'

    usr = UserDetails.objects.get(user_name=username)
    template = loader.get_template('userdetails.html')
    context = {
    'usr': usr,
    }
    return HttpResponse(template.render(context, request))

def updateUserDetails(request, id):
    
    password =  request.POST['password']
    age =  request.POST['age']
    number = request.POST['number']
    usr = UserDetails.objects.get(id = id)
    usr.user_password = password
    usr.user_age = age
    usr.user_phone_no = number 
    usr.save()
    #return render(request, 'login.html')
    return redirect('Authentication:index')


def home(request, username):
    return render (request, 'homepage.html',{'movies':MovieDetails.objects.all(), 'username':username})
