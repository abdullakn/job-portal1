from employee.models import AppliedUsers
from companies.models import CompanyProfile, JobDetails, Subscription
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
from datetime import date

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
    try:
        job=JobDetails.objects.filter().order_by('-closing_date')[:6]
    except:
        job=None    
    try:
        job_count=JobDetails.objects.all().count()  
    except:
        job_count=None      
    try:
        user_count=UserCompanies.objects.filter(company_name=None).count()    
    except:
        user_count=None
    print(user_count)        
    print(job)
    context={
        'jobs':job,
        'job_count':job_count,
        'user_count':user_count
    }
  
    return render(request,'employee/index.html',context)





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
   
    today = date.today()
    try:
        company=CompanyProfile.objects.get(user=request.user)
    except:
        company=None

    try:
        job=JobDetails.objects.filter(user=company).count()
        
        
    except:
        job=None  
      
    try:
        active_job=JobDetails.objects.filter(user=company,closing_date__gte=today).count()
    except:
        active_job=None    

    try:
        appliant_count=AppliedUsers.objects.filter(job__user=company).count()   
    
    except:
        appliant_count=None    

    try:
        subscription=Subscription.objects.get(user=company)  
        print(subscription.subscription_type)
     
    except:
        subscription=None    




    context={
        'job_count':job,
        'active_job':active_job,
        'appliant_count':appliant_count,
        'subscription':subscription

    }    
    

    
    return render(request,'companies/dashboard.html',context)



   
    
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






