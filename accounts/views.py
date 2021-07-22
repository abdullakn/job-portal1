from accounts.models import UserCompanies
from django.shortcuts import render
from django.http import HttpResponse
import uuid

# Create your views here.

def generate_coupen():
    coupen=str(uuid.uuid4()).replace("-","")[:4]
    return coupen

def registration_employee(request):
    if request.method == 'POST':
        data=request.POST
        first_name=data['firstname']
        last_name=data['lastname']
        email=data['email']
        password=data['password']
        code=generate_coupen()
        username=first_name+last_name+code
        
        user=UserCompanies.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
        user.save()
        return HttpResponse("saved")

    return render(request,'employee/register.html')


def registration_companies(request):
    return render(request,'companies/register.html')
