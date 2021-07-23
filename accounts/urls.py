
from django.urls import path
from . import views



urlpatterns = [

    path('employee/register/',views.registration_employee,name='user_registration'),
    path('companies/register/',views.registration_companies,name='companies_registration'),
    path('employee/login/',views.login_employees,name='login_employee'),
    path('companies/login/',views.login_companies,name='login_companies'),
    path('',views.employee_home,name='employee_home'),
    path('companies/home/',views.companies_home,name='companies_home'),
    

]
