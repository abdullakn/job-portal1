from django.contrib.auth import login
from chat.models import Thread
from employee.models import AppliedUsers, EmployeeCV, EmployeeProfile, MachineTestfiles, NeededFilesMachineTest, ReplyMachineTest, SkillBadges, employeePro
from accounts.models import UserCompanies
from companies.models import CompanyExtra, CompanyProfile, CompanySocial, Gallery, JobDetails, JobLocation, Subscription
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseNotFound

#from django.core.mail import send_mail
#from django.core.mail import EmailMessage
import zipfile
from io import BytesIO,StringIO
import os
import uuid

import  stripe


from datetime import date, datetime,date
from datetime import timedelta
from django.contrib import messages
from django.db.models import Q


# Create your views here.




def company_profile(request):
    print("dfdfdfdf")
    if request.method == 'POST':
        print(request.user)
        print("fdfdfdf")
        data=request.POST
        files=request.FILES
        
        if not files:
            try:
                pro=CompanyProfile.objects.get(user=request.user)
                logo=pro.logo
            except:
                logo='\logos\images.png'     
        else:
            logo=files['logo']  
        # if files is None:
        #     pro=CompanyProfile.objects.get(user=request.user)
        #     logo=pro.logo
        # else:
        # if 
        # if CompanyProfile.objects.filter(user=request.user).exists():

        
                
        
        name=data['cname']
        email=data['cemail']
        phone=data['cphone']
        website=data['cwebsite']
        description=data['cdescription']
        country=data['country']
        state=data['state']
        district=data['district']
        pincode=data['postcode']
        twitter=data['twitter']
        facebook=data['facebook']
        google=data['google']
        linkedin=data['linkedin']
        print(twitter,facebook,google)

        print(data)

        if CompanyProfile.objects.filter(user=request.user).exists():
            company=CompanyProfile.objects.get(user=request.user)
            print("asdfghjkl",company)
            
            company.user=request.user
            company.company_name=name
            company.email=email
            company.phone_number=phone
            company.website=website
            company.descriptiion=description
            company.country=country
            company.state=state
            company.district=district
            company.postcode=pincode
            company.logo=logo
            company.save()
            if CompanySocial.objects.filter(user=company).exists():
                website=CompanySocial.objects.get(user=company)
                print("dfghjklfghjk",website)
                print(website.user,website.facebook,website.twitter,website.google)
                print(company,twitter)
                website.user=company
                website.twitter=twitter
                website.facebook=facebook
                website.google=google
                website.linkedin=linkedin
                website.save()
        else:
            company=CompanyProfile(user=request.user,company_name=name,email=email,phone_number=phone,website=website,descriptiion=description,country=country,state=state,district=district,postcode=pincode,logo=logo)
            company.save()
            website=CompanySocial(user=company,twitter=twitter,facebook=facebook,google=google,linkedin=linkedin)
            website.save()


        
        return redirect(company_profile)
    print(request.user) 
    user=UserCompanies.objects.get(username=request.user)
    print(user)
    try:
        profile=CompanyProfile.objects.get(user=user) 
    except CompanyProfile.DoesNotExist:
        profile=None
      
    try:
        website=CompanySocial.objects.get(user=profile) 
    except CompanySocial.DoesNotExist:
        website=None
    try:
        extra=CompanyExtra.objects.get(user=profile)  
    except:
        extra=None      
    context={
        'user':user,
        'profile':profile,
        'website':website,
        'extra':extra
    }
    return render(request,'companies/company_profile.html',context)    



def generate_coupen():
    coupen=str(uuid.uuid4()).replace("-","")[:2]
    return coupen


    
def add_jobs(request):
    if request.method=='POST':
        data=request.POST
        files=request.FILES
        title=data['title']
        job_type=data['job_type']
        category=data['category']
        location=data['location']
        qualification=data['qualification']
        experience=data['experience']
        desc=data['desc']
        skills=data['skills']
        industry=data['industry']
        close_date=data['close_date']
        additional_data=files['additional_data']
        max_sal=data['max_sal']
        min_sal=data['min_sal']
        slug=slugify(str(request.user)+'%'+title)
        print(slug)
        code=generate_coupen()
        title_slug=title+str(code)
        company=CompanyProfile.objects.get(user=request.user)
        job=JobDetails(user=company,job_title=title_slug,job_type=job_type,category=category,location=location,qualification=qualification,experience=experience,description=desc,req_skills=skills,industry=industry,closing_date=close_date,additional_files=additional_data,salary_min=min_sal,salary_max=max_sal,slug=slug)
        job.save()
        loc=JobLocation(user=job,address=location)
        loc.save()
        # user=UserCompanies.objects.get(user=request.user)
        # company=CompanyProfile.objects.get(user=user)
        try:
            plan=Subscription.objects.get(user=company)
            plan.job_remaining-=1
            plan.save()
        except:
            plan=None    
        return redirect('view_jobs')

    try:
        company=UserCompanies.objects.get(username=request.user) 

    except:
        company=None

    try:
        profile=CompanyProfile.objects.get(user=company)  

    except:
        messages.error(request,"First Create the company Profile") 
        return redirect('company_profile')

    try:
        job=JobDetails.objects.filter(user=profile) 

    except:
        job=None

    try:
        subscription=Subscription.objects.filter(user=profile) 

    except:  
        subscription=None                              
    


   


    print(job)
    context={
        'company':company,
        'profile':profile,
        'job':job,
        'count':job.count,
        'subscription':subscription
    }    

        
    return render(request,'companies/add_job.html',context)



def job_listing(request):
    try:
        user=CompanyProfile.objects.get(user=request.user)
    except:
        user=None    
    # print(user.id)
    try:
        job=JobDetails.objects.filter(user=user)
    except:
        job=None    
    print(job)
    context={
        'jobs':job
    }
    return render(request,'companies/job_list.html',context)


def edit_job(request,id):
    job=JobDetails.objects.get(id=id)
    if request.method=='POST':
        data=request.POST
        title=data['title']
        job_type=data['job_type']
        category=data['category']
        location=data['location']
        qualification=data['qualification']
        experience=data['experience']
        desc=data['desc']
        skills=data['skills']
        industry=data['industry']
        close_date=data['close_date']
        max_sal=data['max_sal']
        min_sal=data['min_sal']
        job.job_title=title
        job.job_type=job_type
        job.category=category
        job.location=location
        job.qualification=qualification
        job.experience=experience
        job.description=desc
        job.req_skills=skills
        job.industry=industry
        job.closing_date=close_date
        job.salary_min=min_sal
        job.salary_max=max_sal
        job.save()
        return redirect('view_jobs')
    print(job.closing_date)
    close_date=job.closing_date.strftime('%Y-%m-%d')
    print(close_date)
    context={
        'job':job,
        'close_date':close_date
    }


    return render(request,'companies/edit_job.html',context)    

     

def job_applications(request):
    try:
        user=UserCompanies.objects.get(username=request.user)
        applications=AppliedUsers.objects.filter(job__user__user=user)
    except:
        user=None
        applications=None    
    context={
        'applications':applications,
        
    }
    print(applications)
    return render(request,'companies/job_applications.html',context)




def delete_job(request,id):
    job=JobDetails.objects.get(id=id)
    job.delete()
    return redirect('view_jobs')



def applicant_details(request,id):
    try:
        job=AppliedUsers.objects.get(id=id)
        print("ddddddddddddd",job.user,job)
    except:
        job=None    
   
    try:
        applicant=EmployeeProfile.objects.get(id=job.user.id)
    except:
        applicant=None    
    try:
        propic=employeePro.objects.get(user=applicant)
    except:
        propic=None   
    try:     
        jobs=AppliedUsers.objects.filter(user=job.user)
    except:
        jobs=None
    try:        
        badge=SkillBadges.objects.filter(user=job.user)
    except:
        badge=None    
    # for job in jobs:
    #     print(job.user)
    print(jobs)
    # print(applicant.name)
    context={
        'applicant':applicant,
        'jobs':jobs,
        'propic':propic,
        'badge':badge
    }
    return render(request,'companies/applicants_details.html',context)    



def view_resume(request,id):
    try:
        user=EmployeeProfile.objects.get(id=id)
    except:
        user=None    
    try:
        cv=EmployeeCV.objects.get(user=user)
        mycv=cv.cv
    except:
        cv=None
        mycv=None


    if mycv:    
        response = HttpResponse(mycv, content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"' #user will be prompted with the browser’s open/save file
        response['Content-Disposition'] = 'inline; filename="mycv"' #user will be prompted display the PDF in the browser
        return response
    else:
        return HttpResponseNotFound('This user has no cv')        



def job_applicant_view(request,id):
    job=JobDetails.objects.get(id=id)
    applications=AppliedUsers.objects.filter(job=job)
    print("apppppp",applications)
    context={
        'applications':applications
    }

    return render(request,'companies/view_job_applicants.html',context)



def manage_applications(request,id):
    app=AppliedUsers.objects.get(id=id)
    user=app.user
    job_name=app.job.job_title
    remail=app.user.email
    company=app.job.user.company_name
    job=app.job
    if request.method=='POST':
        machinetest=request.FILES['machinetest']
        github=request.POST.get('github')
        compressed=request.POST.get('compressed')
        host=request.POST.get('host')
        
           
        # else:
        #     github=None    
            
        # if request.POST['compressed']:
        #     compressed="compressed"
        # else:
        #     compressed=None        
          
        # if request.POST['host']:
        #     host="host"
        # else:
        #     host=None        
           

        machine=MachineTestfiles(machinetest=machinetest,user=user,job=job)
        machine.save()

        #create thread for real time chat with machine test users

        print("user machine test",app.user.user.username)
        other_user=UserCompanies.objects.get(id=app.user.user.id)



        if Thread.objects.filter(Q(first_person=request.user,second_person=other_user) | Q(first_person=other_user,second_person=request.user)).exists():
            
            print(request.user)
            print(other_user.username)
            
        else:
            thread_obj=Thread(first_person=request.user,second_person=other_user)
            thread_obj.save()
            print(request.user)
            print(other_user.username)
            

        needed_files=NeededFilesMachineTest(machinetest=machine,github=github,compressed=compressed,host=host)

        needed_files.save()
      
        return redirect('manage_applications' , id=app.id)
    try:
        propic=employeePro.objects.get(user=user)
    except:
        propic=None    
    reply=ReplyMachineTest.objects.filter(machinetest__user=user,machinetest__job=job)
    
    context={'applicant':app,'reply':reply,'propic':propic}
    return render(request,'companies/manage_application.html',context)   



def download_zip(request,id):
    reply=ReplyMachineTest.objects.get(id=id)
    # print('ssss')
    # print(reply.compressed)

    # zip_file = open(reply.compressed, 'r')
    # print(zip_file)
    # response = HttpResponse(zip_file, content_type='application/x-zip-compressed')
    # response['Content-Disposition'] = 'attachment; filename="%s"' % 'foo.zip'
    # return response

    # filelist = reply.compressed
    byte_data = BytesIO()
    # zip_name = "%s.zip" % MyModel.id_no
    zip_file = zipfile.ZipFile(byte_data, 'w')

    # for file in filelist:
    filename = os.path.basename(os.path.normpath(reply.compressed))
    zip_file.write(reply.compressed, filename)
    zip_file.close()

    response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' %'reply'

    zip_file.printdir()

    return response


def add_gallery(request):
    user=UserCompanies.objects.get(username=request.user)
    company=CompanyProfile.objects.get(user=user)
    if request.method=='POST':
        gallery=request.FILES['gallery']
        photo=Gallery(user=company,gallery=gallery)
        photo.save()
        return redirect('company_profile')



def add_extra_company(request):
    user=UserCompanies.objects.get(username=request.user)
    company=CompanyProfile.objects.get(user=user)
    if request.method=='POST':
        company_size=request.POST['size']
        category=request.POST['category']
        founded=request.POST['founded']
        revenue=request.POST['revenue']
        if CompanyExtra.objects.filter(user=company).exists():
            company=CompanyExtra.objects.get(user=company)
            company.company_size=company_size
            company.categorie=category
            company.founded=founded
            company.revenue=revenue
            company.save()
            return redirect('company_profile')

        else:
            comp=CompanyExtra(user=company,company_size=company_size,categorie=category,founded=founded,revenue=revenue)  
            comp.save()
            return redirect('company_profile')



def add_subscription(request):
    return render(request,'companies/subscription_page.html')      







stripe.api_key="sk_test_51JM4m5SH56bFnxNLzkQkET3gIFaIXDTUYP21k5JUlBwhsx3XAbSfko7WLIlFCfBKe2nYHrjvTjagezVKL2tPJxoK00u4eI8Mq6"    

def checkout_session(request):
    session=stripe.checkout.Session.create(
         payment_method_types=['card'],
         line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                'name': 'Normal',
                },
                'unit_amount': int(4.99*10000),
            },
            'quantity': 1,
            }],
             mode='payment',
            success_url='http://127.0.0.1:8000/companies/pay_success/',
            cancel_url='https://example.com/pay_cancel',
    )   
    print(session)
    company=UserCompanies.objects.get(username=request.user)
    user=CompanyProfile.objects.get(user=company)
    today = date.today()
    expiry_date=today+timedelta(days=30)
    if Subscription.objects.filter(user=user).exists():
        subscribe=Subscription.objects.get(user=user)
        subscribe.expiry_date+=timedelta(days=30)
        subscribe.job_remaining+=10
        subscribe.save()
     

    else:    
        subscribe=Subscription(user=user,expiry_date=expiry_date,subscription_type='Normal',job_remaining=10)
        subscribe.save()
  
    return redirect(session.url,code=303) 








def checkout_session_golden(request):
    session=stripe.checkout.Session.create(
         payment_method_types=['card'],
         line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                'name': 'T-shirt',
                },
                'unit_amount': int(799*100),
            },
            'quantity': 1,
            }],
             mode='payment',
            success_url='http://127.0.0.1:8000/companies/pay_success/',
            cancel_url='https://example.com/pay_cancel',
    )   
    print(session)
    company=UserCompanies.objects.get(username=request.user)
    user=CompanyProfile.objects.get(user=company)
    today = date.today()
    expiry_date=today+timedelta(days=60)
  
    if Subscription.objects.filter(user=user).exists():
        subscribe=Subscription.objects.get(user=user)
        subscribe.expiry_date+=timedelta(days=60)
        subscribe.job_remaining+=20
        subscribe.save()

    else:    
        subscribe=Subscription(user=user,expiry_date=expiry_date,subscription_type='Golden',job_remaining=20)
        subscribe.save()
   
    return redirect(session.url,code=303) 









def checkout_session_premium(request):
    session=stripe.checkout.Session.create(
         payment_method_types=['card'],
         line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                'name': 'T-shirt',
                },
                'unit_amount': int(999*100),
            },
            'quantity': 1,
            }],
             mode='payment',
            success_url='http://127.0.0.1:8000/companies/pay_success/',
            cancel_url='https://example.com/pay_cancel',
    )   
    print(session)
    company=UserCompanies.objects.get(username=request.user)
    user=CompanyProfile.objects.get(user=company)
    today = date.today()
    expiry_date=today+timedelta(days=90)
    if Subscription.objects.filter(user=user).exists():
        subscribe=Subscription.objects.get(user=user)
        # print(subscribe.expiry_date)
        subscribe.expiry_date+=timedelta(days=90)
        subscribe.job_remaining+=30
        subscribe.save()

    else:    
        subscribe=Subscription(user=user,expiry_date=expiry_date,subscription_type='Premium',job_remaining=30)
        subscribe.save()
    return redirect(session.url,code=303)      


def pay_success(request):
   return render(request,'companies/payment_success.html')   


def pay_cancel(request):
    return redirect(request,'pay_success.html')            



    
            
   

