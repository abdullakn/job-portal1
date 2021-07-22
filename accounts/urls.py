
from django.urls import path
from . import views


urlpatterns = [

    path('employee/register/',views.registration_employee,name='user_registration'),
    path('companies/register/',views.registration_companies,name='companies_registration'),
    path('employee/login/',views.login_user,name='user_login'),

]
