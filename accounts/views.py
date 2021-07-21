from django.shortcuts import render

# Create your views here.

def registration_employee(request):
    return render(request,'employee/register.html')


def registration_companies(request):
    return render(request,'companies/register.html')
