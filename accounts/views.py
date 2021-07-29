from companies.models import JobDetails
from django.contrib import auth
from django.http.response import JsonResponse
from accounts.models import UserCompanies
from django.shortcuts import redirect, render
from django.http import HttpResponse
# from django.contrib.auth import 
from django.contrib.auth import authenticate,login,logout
import uuid
from django.contrib import messages

from django.db.models import Q

# Create your views here.

def generate_coupen():
    coupen=str(uuid.uuid4()).replace("-","")[:2]
    return coupen

def registration_employee(request):
    if request.user.is_authenticated:
        return redirect('employee_home')
    if request.method == 'POST':
        data=request.POST
        first_name=data['firstname']
        last_name=data['lastname']
        email=data['email']
        password=data['password']
        cpassword=data['cpassword']
        if password != cpassword:
            messages.error(request,"Password is not matched") 

            return redirect('user_registration')
        else:    
            code=generate_coupen()
            username=first_name+last_name+code
            
            user=UserCompanies.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.save()
            messages.success(request,"Registration completed") 

            return redirect('login_employee')

    return render(request,'employee/register.html')


def registration_companies(request):
    if request.method == 'POST':
        data=request.POST
        company_name=data['company_name']
        email=data['email']
        password=data['password']
        cpassword=data['cpassword']
        if password != cpassword:
            messages.error(request,"Password is not matched") 
            return redirect('companies_registration')
        else:    
            code=generate_coupen()
            username=company_name+code
            company=UserCompanies.objects.create_user(company_name=company_name,email=email,password=password,username=username,is_staff=True)
            company.save()
            messages.success(request,"Registration Successfully Completed") 
            return redirect('login_companies')
    return render(request,'companies/register.html')



def login_employees(request):
    if request.user.is_authenticated:
            return redirect('employee_home')

    if request.method=='POST':
        data=request.POST
        email=data['email']
        password=data['password']
        print(password)
        if UserCompanies.objects.filter(email=email,is_staff=False).exists():
            username=UserCompanies.objects.get(email=email,is_staff=False)
            print(username)
            user=auth.authenticate(username=username,password=password)
            print(user)
        
            
            if user is not None:
                login(request,user)
                return redirect('employee_home')
            else:
                context={'error':"Invalid credentials"}
                return render(request,'employee/login.html',context)
        else:
            messages.error(request,"Invalid credentials") 
            return redirect('login_employee')        
    return render(request,'employee/login.html')






def employee_home(request):
    # if request.method=='POST':
    #     data=request.POST
        
    #     main=data['main']
    #     place=data['place']
    #     category=data['category']
    #     job=JobDetails.objects.filter( Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main) & Q(location__istartswith=place) & Q(category__istartswith=place) ) 
    #     print(job.count())
        
    #     context={'job_list':job}
    #     print(job)
    #     print(main,place,category)
    #     # return redirect('job_list_view')
    #     return render(request,'employee/new-list.html',context)
    return render(request,'employee/index.html')





def login_companies(request):
    if request.method=='POST':
        print("hererere")
        data=request.POST
        email=data['email']
        print(email)
        password=data['password']
        if UserCompanies.objects.filter(email=email,is_staff=True).exists():
            username=UserCompanies.objects.get(email=email,is_staff=True)
            print(username)
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('companies_home')
            else:
                messages.error(request,"Invalid credentials")
                return redirect('login_companies') 


        else:
            messages.error(request,"Invalid credentials") 
            return redirect('login_companies')            


    return render(request,'companies/login.html')    



def companies_home(request):
    return render(request,'companies/dashboard.html')



   
    
def employee_logout(request):
    if request.user.is_authenticated:
        print(request.user)
        logout(request)
        
        return redirect('employee_home') 


 
def companies_logout(request):
    if request.user.is_authenticated:
        print(request.user)
        logout(request)
        
        return redirect('login_companies')         



def block_user(request):
    if request.method == "GET":
        id=request.GET['id']
        print("iddddddddddd",id)
        user=UserCompanies.objects.get(id=id)
        print(user.is_active,"aaasdfghjk")
        user.is_active = not user.is_active
        user.save()
        print(user.is_active)
        
    return JsonResponse({'data':user.is_active})    



def check_email(request):
    if request.method == "GET":
        email=request.GET['email']
        print(email)
        if UserCompanies.objects.filter(email=email).exists():
            return HttpResponse(" not available")
        else:
            return HttpResponse("available")         






