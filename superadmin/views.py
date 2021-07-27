from companies.models import JobDetails
from accounts.models import UserCompanies
from employee.models import AppliedUsers, EmployeeProfile
from django.shortcuts import redirect, render
from  django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_control

# Create your views here.


def login(request):

    if request.session.has_key('admin'):
        return redirect('superadmin_home')
  
        
    if request.method=="POST":

        admin_email="admin@gmail.com"
        admin_password="12345"
        data=request.POST
        email=data["email"]
        passw=data["password"] 
        if admin_email ==  email and admin_password == passw:
            request.session['admin'] = True
            return redirect('superadmin_home')
        else:
            return redirect(login)    

    return render(request,'superadmin/login.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def superadmin_home(request):
    return render(request,'superadmin/index.html')


def view_users(request):   
     us=UserCompanies.objects.filter(is_staff=False)
     users=EmployeeProfile.objects.filter()
     context={
         'users':us
     }
     return render(request,'superadmin/view_users.html',context) 



def view_companies(request):   
     companies=UserCompanies.objects.filter(is_staff=True)
     context={
         'companies':companies
     }
     return render(request,'superadmin/view_companies.html',context) 



def view_applications(request):   
     applications=AppliedUsers.objects.all()
     context={
         'applications':applications
     }
     return render(request,'superadmin/view_applications.html',context) 



def view_jobs(request):   
     jobs=JobDetails.objects.all()
     context={
         'jobs':jobs
     }
     return render(request,'superadmin/view_jobs.html',context) 



def tables(request):
    return render(request,'superadmin/table.html')     