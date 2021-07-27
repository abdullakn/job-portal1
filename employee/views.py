from django.db.models.aggregates import Count, Max
from django.http.response import JsonResponse
from django.shortcuts import render
from companies.models import *
from .models import *
import json
from django.core.serializers import serialize



# Create your views here.

def job_list_view(request):
    
    jobs=JobDetails.objects.all()
    # p=AppliedUsers.objects.all().aggregate(Max(Count('job')))
    # p = JobDetails.objects.all().annotate(Count('AppliedUsers__job', distinct=True))
    # q = AppliedUsers.objects.filter(AppliedUsers.objects.values('job').distinct())
    # print("ddddddddddd",p)
    # app=AppliedUsers.objects.aggregate(Max('job'))
    application=AppliedUsers.objects.all()
    print("ddfdfdfdf",application.count())
    print(application.count())
    for app in application:
        
        for job in jobs:
            if job == app.job:
                print(app)
    context={
        'job_list':jobs
    }
    return render(request,'employee/job-listings.html',context)    


def job_detail_view(request,slug):
    job=JobDetails.objects.get(slug=slug)
    str=job.req_skills
    tag_list = str.split(",")
    print(tag_list)
    try:
        user=EmployeeProfile.objects.get(user=request.user)
        applied=AppliedUsers.objects.filter(user=user,job=job)
    except:
        user=None
        applied=None

    context={
        'user':user,
        'applied':applied,
        'jobs':job,
        'tag_list':tag_list
    }
    return render(request,'employee/job_details.html',context)   



def employee_profile(request):
    if request.method=='POST':
        data=request.POST
        name=data['name']
        email=data['email']
        phone=data['phone']
        age=data['age']
        place=data['place']
        education=data['education']
        if EmployeeProfile.objects.filter(user=request.user).exists():
            employee=EmployeeProfile.objects.get(user=request.user)
            employee.name=name
            employee.email=email
            employee.phone=phone
            employee.age=age
            employee.place=place
            employee.education=education
            employee.save()
        else:
            employee=EmployeeProfile(user=request.user,name=name,email=email,phone=phone,age=age,place=place,education=education)    
            employee.save()


    try:
        employee=EmployeeProfile.objects.get(user=request.user)
    except:
        employee=None   

    context={
        'employee':employee
    }         
        
    return render(request,'employee/employee_profile.html',context)     



def applyJob(request):
    if request.method == "GET":
        id=request.GET['id']
        job=JobDetails.objects.get(id=id)
        user=EmployeeProfile.objects.get(user=request.user)
        applied_user=AppliedUsers(user=user,job=job)
        applied_user.save()
        print(job)
    return JsonResponse({'data':"success"})   




def company_list(request):
    try:
        company=CompanyProfile.objects.all() 
    except:
        company=None
    context={
        'company':company
    }
    return render(request,'employee/companies_list.html',context)   


def search_company(request):
    print("data vvv")
    if request.method == "GET":
        search_string=request.GET['search']
        print(search_string)
        try:
            company=CompanyProfile.objects.filter(company_name__icontains=search_string).values()
        except:
            company=None    
        print("dddd",company.values())
        data=company.values()
        
        
        return JsonResponse(list(data),safe=False)  



def companies_details(request,id):
    company=CompanyProfile.objects.get(id=id)
    job=JobDetails.objects.filter(user=company)
    context={
        'company':company,
        'job':job
    }
    return render(request,'employee/companies_details.html',context)        
     

    
