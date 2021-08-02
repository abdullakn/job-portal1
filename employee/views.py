from django.http import response
from superadmin.models import Question
from django.db.models.aggregates import Count, Max
from django.http import request
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from companies.models import *
from .models import *
import json
from django.core.serializers import serialize
from django.db.models import Q
from django.template.loader import render_to_string

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import Count,Min,Max,Avg
from django.core.files.base import ContentFile
import base64




# Create your views here.





def job_list_view(request):

    if request.method=='POST':
        pass
    
    jobs=JobDetails.objects.all()
    print(jobs)
    p=AppliedUsers.objects.all().aggregate(Count('job'))
   
    print("ddddddddddd",p)
    
    # p = JobDetails.objects.all().annotate(Count('job',distinct=True))
    app=AppliedUsers.objects.aggregate(Count('user'))
    print("aaaa",app)
    application=AppliedUsers.objects.all()
    print("ddfdfdfdf",application)
    print(application.count())
    count_application =AppliedUsers.objects.all().annotate(Count('job',distinct=True))
    print("count",count_application)

    count = AppliedUsers.objects.values('job').distinct()
    print(count)

    count_new=AppliedUsers.objects.all().values('job').annotate(count=Count('job', distinct=True)).order_by()
    print("count new",count_new)


    annotate=JobDetails.objects.annotate(Count('appliedusers__job'))

    print("annotate",annotate)

    co=AppliedUsers.objects.all().annotate(Count('job__job_title')).distinct()
    print("cooooo",co)

    filt=AppliedUsers.objects.filter().distinct('job')
    print("filtrrr",filt)

    #get the application of each job


    obj=AppliedUsers.objects.values('job','job__id').annotate(the_count=Count('job'))
    

    print("aasdfghjkl",obj)

    #get the hotest job in the site based on most apllications

    max_applicants=obj.order_by('job')[0]
    print("max applicant",max_applicants)
    employee=EmployeeProfile.objects.get(user=request.user)
    favourite=FavouriteJob.objects.filter(user=employee)
    
    context={
        'job_list':jobs,
        'app_count':obj,
        'max_applicants':max_applicants,
        'favourite':favourite
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

    try:
        favourite=FavouriteJob.objects.get(job=job)  
    except:
        favourite=None      

    context={
        'user':user,
        'applied':applied,
        'jobs':job,
        'tag_list':tag_list,
        'favourite':favourite
    }
    return render(request,'employee/job_details.html',context)   



def employee_profile(request):
    print("default")
    if request.method=='POST':
        print("post")
        data=request.POST
        name=data['name']
        email=data['email']
        phone=data['phone']
        age=data['age']
        place=data['place']
        education=data['education']
        gender=data['gender']
        spec=data['specialization']
        desc=data['description']
        experience=data['experience']
        dob=data['dob']
        print(spec,dob,desc,experience,gender)
        if EmployeeProfile.objects.filter(user=request.user).exists():
            employee=EmployeeProfile.objects.get(user=request.user)
            employee.name=name
            employee.email=email
            employee.phone=phone
            employee.age=age
            employee.place=place
            employee.education=education
            employee.gender=gender
            employee.specialization=spec
            employee.description=desc
            employee.experience=experience
            employee.dob=dob
            employee.save()
            print(employee)
            print("fghjghj")
        else:
            employee=EmployeeProfile(user=request.user,name=name,email=email,phone=phone,age=age,place=place,education=education,gender=gender,experience=experience,dob=dob,
                                      specialization=spec, description=desc)    
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
    # try:
    company=CompanyProfile.objects.all() 
    for comp in company:
        print(comp.logo,comp.company_name)

    print("ccccssssssssssssssssssssssssssssssssssssssssssssssssss",company)
    # except:
    #     company=None
    #     print(company)
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



def search_jobs(request):   
    main=request.GET['main']
    place=request.GET['place']
    category=request.GET['category']
    print(main,place,category)
    job=JobDetails.objects.filter( Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main) & Q(location__istartswith=place) & Q(category__istartswith=place) ) 
    print(job.count())
    
    context={'job_list':job}
    print(job)
    print(main,place,category)
    # return redirect('job_list_view')
    return render(request,'employee/new-list.html',context)
    # return HttpResponse("success")



def filter_data(request):
    print("success")
    location=request.GET.getlist('location[]')
    jobtype=request.GET.getlist('jobtype[]')
    category=request.GET.getlist('category[]')
    print(location,jobtype,category)
    allJobs=JobDetails.objects.all().order_by('-id')
    if len(location)>0 or len(jobtype)>0 or len(category)>0:
        allJobs=JobDetails.objects.filter(Q(location__in=location)|Q(job_type__in=jobtype)|Q(category__in=category))
        
    # if len(jobtype)>0:
    #     allJobs=JobDetails.objects.filter(Q(job_type__in=jobtype))
        
    # if len(category)>0:
    #     allJobs=JobDetails.objects.filter(Q(category__in=category))
        
    data=render_to_string('employee/filter-list.html',{'job_list':allJobs})
    return JsonResponse({'data':data})    


def view_pdf(request,id):
    fs=FileSystemStorage()
    print("fffffffffff",fs)
    mypdf=JobDetails.objects.get(id=id)
    print("fffffffffff",mypdf)
    filename1='job_additional/sslc_2hqnCa0.pdf'
    filename=mypdf.additional_files
    print("fffffffffff",filename)
    print("fffffffffff",filename1)
    # if fs.exists(filename):
        # with fs.open(filename) as pdf:
    if filename:    
        response = HttpResponse(filename, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
        response['Content-Disposition'] = 'inline; filename="filename"' #user will be prompted display the PDF in the browser
        return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')



def cv_management(request):
    if request.method == 'POST':
        data=request.FILES
        newcv=data['mycv']
        user=EmployeeProfile.objects.get(user=request.user)

        if EmployeeCV.objects.filter(user=user).exists():
            cvobj=EmployeeCV.objects.get(user=user)
            cvobj.cv=newcv
            cvobj.save()
            return redirect('make_cv')
        else:
            cvobj=EmployeeCV(user=user,cv=newcv)   
            cvobj.save() 
            return redirect('make_cv')
    return render(request,'employee/make_cv.html')   



def view_cv(request):
    user=EmployeeProfile.objects.get(user=request.user)
    try:
        cv=EmployeeCV.objects.get(user=user) 
        mycv=cv.cv  
    except:
        mycv=None    
    
    if mycv:    
        response = HttpResponse(mycv, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
        response['Content-Disposition'] = 'inline; filename="mycv"' #user will be prompted display the PDF in the browser
        return response
    else:
        return HttpResponseNotFound('This user has no cv')   




def employee_badge(request):
    question=Question.objects.all()
    context={'question':question}
    return render(request,'employee/employee_badge.html',context)    



def employee_applied_list(request):
    user=EmployeeProfile.objects.get(user=request.user)
    jobs=AppliedUsers.objects.filter(user=user)
    context={'jobs':jobs}
    return render(request,'employee/employee_appliedjobs.html',context)     



def favourite_jobs(request,id):
    job=JobDetails.objects.get(id=id)
    user=EmployeeProfile.objects.get(user=request.user)
    favourite=FavouriteJob(user=user,job=job)
    favourite.save()
    return redirect('job_detail_view', id=job.slug)

def view_favourite(request):
    user=EmployeeProfile.objects.get(user=request.user)
    favourite=FavouriteJob.objects.filter(user=user) 
    context={
        'favourite':favourite
    } 
    return render(request,'employee/favourite_jobs.html',context)


def view_machinetest(request):
    user=EmployeeProfile.objects.get(user=request.user)
    machine=MachineTestfiles.objects.filter(user=user)
    print(machine)
    context={
        'machine':machine
    }
    return render(request,'employee/machinetest.html',context) 


def download_machinetest(request,id):
    file=MachineTestfiles.objects.get(id=id)
    mypdf=file.machinetest
    # if mypdf:
    #     with open(mypdf,'rb') as fh:
    #         response=HttpResponse(fh.read(),content_type="application/pdf")
    #         response['Content-Disposition'] = 'inline; filename="mycv"'
    #         return response

    # raise Http404        

    if mypdf:    
        response = HttpResponse(mypdf, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
        response['Content-Disposition'] = 'inline; filename="mypdf"' #user will be prompted display the PDF in the browser
        return response
    else:
        return HttpResponseNotFound('This user has no cv')  



def propic_save(request):
    print("submitted")
    # if request.method == "GET":
    #     image=request.GET['image']
        
      
    #     format, img4 = image.split(';base64,')
    #     ext = format.split('/')[-1]
    #     img_data4 = ContentFile(base64.b64decode(img4), name="pro_pic" + '4.' + ext)
    #     print("final imageddddddddddddddddddddddddddddddddddddddddddddddddd",img_data4)
    #     user=EmployeeProfile.objects.get(user=request.user)
    #     propic=employeePro(user=user)
    #     propic.save()
       
        # return JsonResponse({'data':"success"})         











     

    
