from django.contrib import auth
from accounts.models import UserCompanies
from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth import 
from django.contrib.auth import authenticate,login,logout
import uuid

# Create your views here.

def generate_coupen():
    coupen=str(uuid.uuid4()).replace("-","")[:3]
    return coupen

def registration_employee(request):
    if request.method == 'POST':
        data=request.POST
        first_name=data['firstname']
        last_name=data['lastname']
        email=data['email']
        password=data['password']
        code=generate_coupen()
        username=first_name+last_name+code
        
        user=UserCompanies.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
        user.save()
        return HttpResponse("saved")

    return render(request,'employee/register.html')


def registration_companies(request):
    if request.method == 'POST':
        data=request.POST
        company_name=data['company_name']
        email=data['email']
        password=data['password']
        code=generate_coupen()
        username=company_name+code
        company=UserCompanies.objects.create_user(company_name=company_name,email=email,password=password,username=username,is_Staff=True)
        company.save()
        return HttpResponse("saved")
    return render(request,'companies/register.html')



def login_user(request):


    
    if request.method=='POST':
        data=request.POST
        email=data['email']
        print(email)
        
        password=data['password']
        print(password)
        username=UserCompanies.objects.get(email=email)
        print(username)
        user=auth.authenticate(username=username,password=password)
        print(user)
       
        
        if user is not None:
            login(request,user)
            return render(request,'employee/index.html')
        else:
            return render(request,'employee/login.html')
    return render(request,'employee/login.html')




