from django.urls import path
from . import views



urlpatterns = [


    path('add_job/',views.add_jobs,name='add_jobs'),
    path('profile/',views.company_profile,name='company_profile'),
 
    

]
