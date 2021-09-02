from io import BytesIO
from django import template
from django.contrib.auth.models import AnonymousUser
# from django.db.models.expressions import Random
from django.http import response
from geocoder.api import location
from superadmin.models import CategoryDomain, Question
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
from .form import CoverletterForm
from django.template.loader import get_template
from django.core.paginator import EmptyPage, InvalidPage, Paginator
import random
from django.core.mail import EmailMessage, message
from django.contrib import messages
import random
# import pdfkit
# from io import BytesIO,StringIO
# from xhtml2pdf import pisa




# import datetime
# from weasyprint import HTML
# import tempfile
# from django.db.models import Sum


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# from io import BytesIO
# from django.template.loader import get_template
# import xhtml2pdf.pisa as pisa


from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib





# Create your views here.


userans_list=[]




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
    try:

        max_applicants=obj.order_by('job')[0]
    except:
        max_applicants=None    
    print("max applicant",max_applicants)
    try:
        employee=EmployeeProfile.objects.get(user=request.user)        
    except:
        employee=None

    try:
        applied=AppliedUsers.objects.filter(user=employee)    
    except:
        applied=None   

    print("applied123",applied)       

    for job in jobs:
    
            for appl in applied:
          
                if job.id == appl.job.id:
                    print(appl,"hhhhh")
    
        
    context={
        'job_list':jobs,
        'app_count':obj,
        'max_applicants':max_applicants,
        'applied':applied
    }
    return render(request,'employee/job-listings.html',context)    


def job_detail_view(request,slug):
    job=JobDetails.objects.get(slug=slug)
    try:
        loc=JobLocation.objects.get(user=job)
    except:
        loc=None    
    str=job.req_skills
    tag_list = str.split(",")
    print(tag_list)
    try:
        user=EmployeeProfile.objects.get(user=request.user)
    except:
        user=None    
    try:    
        applied=AppliedUsers.objects.filter(user=user,job=job)
        
        
    except:
        
        applied=None

    try:
        favourite=FavouriteJob.objects.get(job=job,user=user)  
    except:
        favourite=None      

    try:
        cv=EmployeeCV.objects.get(user=user)  
    except:
        cv=None      

    context={
        'user':user,
        'applied':applied,
        'jobs':job,
        'tag_list':tag_list,
        'favourite':favourite,
        'location':loc,
        'cv':cv
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

    try:
        propic=employeePro.objects.get(user=employee) 
    except:
        propic=None       

    context={
        'employee':employee,
        'propic':propic
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
        'company':company,
        
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
    try:
        company=CompanyProfile.objects.get(id=id)
    except:
        company=None
    try:
        job=JobDetails.objects.filter(user=company)
    except:
        job=None    
    try:    
        photos=Gallery.objects.filter(user=company)
    except:  
        photos=None  
    try:    
        extra=CompanyExtra.objects.get(user=company)
    except:
        extra=None    
    try:
        social=CompanySocial.objects.get(user=company)  
    except:
        social=None      
    print(photos)
    context={
        'company':company,
        'job':job,
        'photos':photos,
        'extra':extra,
        'social':social
    }
    return render(request,'employee/companies_details.html',context)        



def search_jobs(request):   
    main=request.GET['main']
    place=request.GET['place']
    category=request.GET['category']
    print(main,type(place),category)
    print(category,"category")
    if main != "" and place !="" and category != "":
        print("inside if ")
        job=JobDetails.objects.filter( Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main)) & JobDetails.objects.filter(location__istartswith=place)  & JobDetails.objects.filter(category__istartswith=category) 
    # allJobs=JobDetails.objects.filter(Q(location__in=place)|Q(job_type__in=jobtype)|Q(category__in=category))
    elif main!="" and place =="" and category=="":
        print("main only")
        job=JobDetails.objects.filter(Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main))
    elif  main=="" and place =="" and category!="": 
        print("category only")
        job=JobDetails.objects.filter(category__istartswith=category)  
    elif  main=="" and place !="" and category=="": 
        print("place only")
        job=JobDetails.objects.filter(location__istartswith=place) 
    elif main!="" and place !="" and category=="":
        print("main and place only")
        job=JobDetails.objects.filter(Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main)) & JobDetails.objects.filter(location__istartswith=place)   
    elif main!="" and place =="" and category!="":
        print("main and category only")
        job=JobDetails.objects.filter(Q(job_title__istartswith=main) | Q(user__company_name__istartswith=main)) & JobDetails.objects.filter(category__istartswith=category)  
    elif main=="" and place !="" and category!="":
        print("place and category only")
        job=JobDetails.objects.filter(location__istartswith=place)  & JobDetails.objects.filter(category__istartswith=category)  

    else:
        print("inside else ")
        job=JobDetails.objects.all()
        # job=JobDetails.objects.filter(Q(location__istartswith=place) & Q(category__istartswith=category))
    print(job.count())
    
    context={'job_list':job,'main':main,'place':place,'category':category}
    print(job)
    print(main,place,category)
    # return redirect('job_list_view')
    return render(request,'employee/new-list.html',context)
  



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
        try:
            user=EmployeeProfile.objects.get(user=request.user)
        except:
            return redirect('employee_profile')    

        if EmployeeCV.objects.filter(user=user).exists():
            cvobj=EmployeeCV.objects.get(user=user)
            cvobj.cv=newcv
            cvobj.save()
            return redirect('make_cv')
        else:
            cvobj=EmployeeCV(user=user,cv=newcv)   
            cvobj.save() 
            return redirect('make_cv')
    form=CoverletterForm() 
    try:
        user=EmployeeProfile.objects.get(user=request.user)
        education=EducationDetails.objects.filter(user=user)
        experience=ExperienceDetails.objects.filter(user=user)
        skills=SkillsDetails.objects.filter(user=user)
        awards=AwardsDetails.objects.filter(user=user)
        # print("in try",education,experience)
    except:
        print("hello")
        messages.error(request,"First Create the Basic Information ") 
        return redirect('employee_profile')

    try:
        education=EducationDetails.objects.filter(user=user)
    except:
        education=None    
    try:
        experience=ExperienceDetails.objects.filter(user=user)
    except:
        experience=None    
    try:
        skills=SkillsDetails.objects.filter(user=user)
    except:
        skills=None   
    try:
        awards=AwardsDetails.objects.filter(user=user)
    except:
        awards=None   

    print(awards,education,experience,skills)    
         

    
    # print(form)
    context={'form':form,'education':education,'experience':experience,'awards':awards,'skills':skills}
    return render(request,'employee/make_cv.html',context)   






def view_cv(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
    except:
        return redirect('employee_profile')    
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



 



def employee_applied_list(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
        jobs=AppliedUsers.objects.filter(user=user)
    except:
        jobs=None    
    context={'jobs':jobs}
    return render(request,'employee/employee_appliedjobs.html',context)     



def favourite_jobs(request,id):
    print("favvvvvvvvvv",request.user)
    if not request.user.is_authenticated:
        print("hello")
        return redirect('login_employee')
    try:
        job=JobDetails.objects.get(id=id)
        user=EmployeeProfile.objects.get(user=request.user)
    except EmployeeProfile.DoesNotExist: 
        return redirect('employee_profile')   

    favourite=FavouriteJob(user=user,job=job)
    favourite.save()
    return redirect('job_details', slug=job.slug)

def view_favourite(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
    except:
        user=None  
    try:      
        favourite=FavouriteJob.objects.filter(user=user) 
    except:
      
        favourite=None  
    try:    
        favourite=FavouriteJob.objects.filter(user=user) 
    except:
        favourite=None    
    context={
        'favourite':favourite
    } 
    return render(request,'employee/favourite_jobs.html',context)


def view_machinetest(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
        machine=MachineTestfiles.objects.filter(user=user)
    except:
        machine=None    
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
    user=UserCompanies.objects.get(username=request.user)
    try:
        employee=EmployeeProfile.objects.get(user=user)
    except:
        messages.success(request,"First Create the Basic Information ") 
        return redirect('employee_profile')    
    print(user)
    print(employee)
    if request.method=='POST':
        image=request.FILES['image']
        if employeePro.objects.filter(user=employee).exists():
            propic=employeePro.objects.get(user=employee)
            propic.pro_pic=image
            propic.save()
            return redirect('employee_profile')
        else:
            propic=employeePro(user=employee,pro_pic=image)   
            propic.save() 
            return redirect('employee_profile')


  


def make_coverletter(request):
    print("asdfffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
    user=EmployeeProfile.objects.get(user=request.user)


    if request.method=='POST':
         form=CoverletterForm(request.POST)
         print("outside",form)
         if form.is_valid():
            coverletter=form.cleaned_data['coverletter']
            if CoverLetter.objects.filter(user=user).exists():
                coverletter=CoverLetter.objects.get(user=user)
                coverletter.coverletter=coverletter
                return redirect('make_cv')
            else:    
           
                print("coverletter",coverletter)
                letter=CoverLetter(user=user,coverletter=coverletter)
                letter.save()
                return redirect('make_cv')

def add_education(request):
    user=EmployeeProfile.objects.get(user=request.user)
    if request.method=='POST':
        data=request.POST 
        title=data['title']
        startyear=data['startyear']
        endyear=data['endyear']
        institute=data['institute'] 
        education=EducationDetails(user=user,title=title,startyear=startyear,endyear=endyear,institute=institute)  
        education.save()
        return redirect('make_cv')   


def add_experience(request):
    user=EmployeeProfile.objects.get(user=request.user)
    if request.method=='POST':
        data=request.POST
        title=data['title']
        years=data['years']
        company=data['company']   
        experience=ExperienceDetails(user=user,title=title,years=years,company=company)
        experience.save()
        return redirect('make_cv')   


def add_skills(request):
    user=EmployeeProfile.objects.get(user=request.user)
    
    if request.method=='POST':
        data=request.POST
        skill=data['skill']
        percentage=data['percentage']
        skill=SkillsDetails(user=user,skill=skill,percentage=percentage)
        skill.save()
        return redirect('make_cv')


def add_awards(request):
    user=EmployeeProfile.objects.get(user=request.user)
    
    if request.method=='POST':
        data=request.POST
        award=data['award']
        years=data['years']
        company=data['company']
        award=AwardsDetails(user=user,award=award,years=years,company=company)
        award.save()
        return redirect('make_cv')


def load_cv(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
    except:
        user=None   
    try:     
        education=EducationDetails.objects.filter(user=user)
    except:    
        education=None
    try:    
        experience=ExperienceDetails.objects.filter(user=user)
    except:
        experience=None    
    try:    
        skills=SkillsDetails.objects.filter(user=user)
    except:
        skills=None  
    try:      

        awards=AwardsDetails.objects.filter(user=user)
    except:
        awards=None    
    try:    
        coverletter=CoverLetter.objects.get(user=user)
    except:
        coverletter=None 
    try:       
        propic=employeePro.objects.get(user=user)
    except:
        propic=None    
   
  
    context={'user':user,'education':education,'experience':experience,'awards':awards,'skills':skills,'coverletter':coverletter,'propic':propic}
    return render(request,'employee/cv_template.html',context) 

    




def employee_badge(request,id):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
    except:
        messages.error(request,"Please Fill the Employee Profile First")
        return redirect('employee_profile')    
    category=CategoryDomain.objects.get(id=id)
    request.session['category']=category.category
   
    # question=Question.objects.filter(category=id)[:6]
    question=Question.objects.filter(category=id)[:5]
    print(question)
    q_list=list(question)
    random.shuffle(q_list)


    final_list=q_list
    print("final list",question)
    
   
    
    


    count=0
    for quest in question:
        request.session['answer'+str(count)]=quest.answer
        count=count+1
        print(quest)

    paginator=Paginator(question,1)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        questions=paginator.page(page)
    except(EmptyPage,InvalidPage):
        questions=paginator.page(paginator.num_pages)

      

    context={'question':question,'questions':questions}
    return render(request,'employee/employee_badge.html',context)  





def saveans(request):
    print("defhfdfd")
    if request.method == "GET":
        ans=request.GET['ans']
        print("asdfghjkk",ans)
        userans_list.append(ans)
        return JsonResponse({'data':"success"},safe=False)


def submit_answers(request):
    print("session",request.session['answer0'])
    print("session",request.session['answer1'])
    print("session",request.session['answer2'])
    print("session",request.session['answer3'])
    print("session",request.session['answer4'])

    for li in userans_list:
        print("userrrrr",li)
    obj=Question.objects.all()[:5]
    score=0
    # answers=[]
    # for ans in obj:
    #     answers.append(ans.answer)
    #     print(ans.answer)

    for i in range(5):
        if request.session['answer'+str(i)] == userans_list[i]:
            print(userans_list[i],request.session['answer'+str(i)])
            score=score+1
            print("session",request.session['answer'+str(i)])

    userans_list.clear()   

    score=score+score   
    
    user=EmployeeProfile.objects.get(user=request.user)
    cate=request.session['category']
    category=CategoryDomain.objects.get(category=cate)
    
    if score >= 6:
        print("data")
        if SkillBadges.objects.filter(user=user,category=category).exists():
            print("dataddd")
            if score >= 8:
                print("datajjjj")
                badge=SkillBadges.objects.get(user=user,category=category)
                badge.score=score
                badge.badge='Gold'
                badge.save()
        else:
            print("ggggg")
            if score >= 8:
                print("ddddfd")
                badge=SkillBadges(user=user,category=category,badge='Gold',score=score) 
                badge.save()


            elif score >= 6:
                print("dfdfdfdfdfff")
                badge=SkillBadges(user=user,category=category,badge='Silver',score=score) 
                badge.save()
                
            else:
                pass    
  

    return render(request,'employee/congratulation.html',{'score':score})  



def badges(request):
    try:
        user=EmployeeProfile.objects.get(user=request.user)
        badge=SkillBadges.objects.filter(user=user)
    except:
        badge=None    
    context={
        'badges':badge
    }
    return render(request,'employee/badge.html',context)     


def reply_machine_test(request,id):
    test=MachineTestfiles.objects.get(id=id)
    comp_email=test.job.user.email
    user=test.user.name
    job_name=test.job.job_title
    needed=NeededFilesMachineTest.objects.get(machinetest=test)
    if request.method=='POST':
        compressed=request.FILES.get('compressed', None)
        github=request.POST.get('github', None)
        print(compressed,github)
        host=request.POST.get('host', None)
        
        print(host)
        email=EmailMessage('Machine Test completed Sended from',user + " send the machine test of "+ job_name,
                  'abdudebanjazz@gmail.com', [comp_email])
        # email.content_subtype='html'  
        # email.attach(compressed)  
        email.send()   

      
        reply=ReplyMachineTest(machinetest=test,compressed=compressed,github=github,host=host)
        reply.save()
          
        
        return redirect('machine_test')
    context={'needed':needed}

    return render(request,'employee/reply_machine_test.html',context)  



def delete_machinetest(request,id):
    machine=MachineTestfiles.objects.get(id=id)
    machine.delete()
    return redirect('machine_test')     


def delete_favourite(request,id):
    favourite=FavouriteJob.objects.get(id=id)
    favourite.delete()   
    return redirect('view_favourite')    


def delete_education(request,id):  
    education=EducationDetails.objects.get(id=id)
    education.delete()   
    return redirect('make_cv') 

def delete_experience(request,id):  
    experience=ExperienceDetails.objects.get(id=id)
    experience.delete()   
    return redirect('make_cv')     



def delete_skill(request,id):
    skill=SkillsDetails.objects.get(id=id)
    skill.delete()   
    return redirect('make_cv')   


def delete_awards(request,id):
    award=AwardsDetails.objects.get(id=id)
    award.delete()   
    return redirect('make_cv')          


  



# def category_wise_list(request,category):

#     return render(request,'employee/job-listings.html',context)        


















     

    
