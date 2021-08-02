from employee.models import AppliedUsers, EmployeeCV, EmployeeProfile, MachineTestfiles
from accounts.models import UserCompanies
from companies.models import CompanyProfile, CompanySocial, JobDetails
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseNotFound


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
    context={
        'user':user,
        'profile':profile,
        'website':website
    }
    return render(request,'companies/company_profile.html',context)    




    
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
        company=CompanyProfile.objects.get(user=request.user)
        job=JobDetails(user=company,job_title=title,job_type=job_type,category=category,location=location,qualification=qualification,experience=experience,description=desc,req_skills=skills,industry=industry,closing_date=close_date,additional_files=additional_data,salary_min=min_sal,salary_max=max_sal,slug=slug)
        job.save()
        return redirect(job_listing)

        
    return render(request,'companies/add_job.html')



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


def job_applications(request):
    try:
        user=UserCompanies.objects.get(username=request.user)
        applications=AppliedUsers.objects.filter(job__user__user=user)
    except:
        user=None
        applications=None    
    context={
        'applications':applications
    }
    print(applications)
    return render(request,'companies/job_applications.html',context)




def delete_job(request,id):
    job=JobDetails.objects.get(id=id)
    job.delete()
    return redirect('view_jobs')



def applicant_details(request,id):
    job=AppliedUsers.objects.get(id=id)
    print("ddddddddddddd",job.user,job)
    applicant=EmployeeProfile.objects.get(id=job.user.id)
    jobs=AppliedUsers.objects.filter(user=job.user)
    for job in jobs:
        print(job.user)
    print(jobs)
    print(applicant.name)
    context={
        'applicant':applicant,
        'jobs':jobs
    }
    return render(request,'companies/applicants_details.html',context)    



def view_resume(request,id):
    user=EmployeeProfile.objects.get(id=id)
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
    job=app.job
    if request.method=='POST':
        machinetest=request.FILES['machinetest']
        machine=MachineTestfiles(machinetest=machinetest,user=user,job=job)
        machine.save()
        return redirect('manage_applications' , id=app.id)
    
    
    
    context={'applicant':app}
    return render(request,'companies/manage_application.html',context)    




