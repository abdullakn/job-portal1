from django.shortcuts import render

# Create your views here.


def add_jobs(request):
    return render(request,'companies/add_job.html')


def company_profile(request):
    return render(request,'companies/company_profile.html')    
