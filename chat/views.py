from superadmin.views import login
from companies.models import CompanyProfile
from employee.models import EmployeeProfile, employeePro
from django.http.response import HttpResponse
from chat.models import Thread
from django.shortcuts import render
from .models import *

# Create your views here.


def messages_pages(request):
    print("login user..............",request.user)
    threads=Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    user=UserCompanies.objects.get(username=request.user)
    if user.company_name:
        profile=EmployeeProfile.objects.all()
        try:
            pro_pic=employeePro.objects.all()
        except:
            pro_pic=None
        login_pro=CompanyProfile.objects.get(user=request.user)    
        print("loggggg",login_pro.logo)    
        print(pro_pic)
        print("company",profile)
    else:
        
        profile=CompanyProfile.objects.all() 
        pro_pic=None 
        try:
            user=EmployeeProfile.objects.get(user=request.user)
        except:
            None    
        try:
            login_pro=employeePro.objects.get(user=user)
        except:
            login_pro=None    
        
        print("student",profile)  


        

    for thread in threads:   
        for pro in profile:   
            if thread.second_person.id == pro.user.id:
                print("2")
                for pic in pro_pic:
                    if thread.second_person.id == pic.user.user.id:
                        print("user",pic)
        
    context={
        'Threads':threads,
        'profile':profile,
        'pro_pic':pro_pic,
        'login_pro':login_pro
    }
    print(threads)
    return render(request,'messages.html',context)

def create_thread(request):
    if request.method=='POST':
        other=request.POST['other']
        other_user=UserCompanies.objects.get(id=other)
        if Thread.objects.filter(Q(first_person=request.user,second_person=other_user) | Q(first_person=other_user,second_person=request.user)).exists():
            
            print(request.user)
            print(other_user.username)
            return HttpResponse("exist")
        else:
            thread_obj=Thread(first_person=request.user,second_person=other_user)
            thread_obj.save()
            print(request.user)
            print(other_user.username)
            return HttpResponse("not exist")    


    user=UserCompanies.objects.all()
    context={
        'user':user
    }
    return render(request,'create_thread.html',context)    
