from companies.models import JobDetails
from accounts.models import UserCompanies
from employee.models import AppliedUsers, EmployeeProfile
from django.shortcuts import redirect, render
from  django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_control
from django.utils.text import slugify
from .models import CategoryDomain, models,Question
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


def add_category(request):
    cat_all=CategoryDomain.objects.all()

    if request.method == 'POST':
        category=request.POST['category']
        slug=slugify(category)
        if CategoryDomain.objects.filter(category=category).exists():
            cat=CategoryDomain.objects.get(category=category)
            cat.category=category
            cat.save()
        else:    
            cat=CategoryDomain(category=category,slug=slug)
            cat.save()
        cat_all=CategoryDomain.objects.all()
      
        return redirect('add_category')
    
    print(cat_all)
    context={
        'category':cat_all
    }    
    return render(request,'superadmin/add_category.html',context)     


def add_questions(request,id):
    if request.method == 'POST':
        data=request.POST
        question=data['question']
        option1=data['option1']
        option2=data['option2']
        option3=data['option3']
        option4=data['option4']
        ans=data['answer']
        if ans == 'option1':
            answer=option1
        elif ans == 'option2':
            answer=option2
        elif ans == 'option3':
            answer=option3
        else:
            answer=option4
        category=request.session['category']
        cat_obj=CategoryDomain.objects.get(category=category)
        id=cat_obj.id
        question=Question(category=cat_obj,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer)
        question.save()
        
        return redirect('add_questions', id=cat_obj.id )
        
    category=CategoryDomain.objects.get(id=id)
    print(category)
    request.session['category']=category.category
    print("session", request.session['category'])
    return render(request,'superadmin/add_questions.html')


