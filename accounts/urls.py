
from django.urls import path
from . import views


urlpatterns = [

    path('employee/register/',views.registration_employee,name='registration'),
    path('companies/register/',views.registration_companies,name='registration'),
]
