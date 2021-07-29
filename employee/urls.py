from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [


    path('job_list/',views.job_list_view,name='job_list_view'),
    path('job_details/<slug:slug>/',views.job_detail_view,name='job_details'),
    path('profile/',views.employee_profile,name='employee_profile'),
    path('applyJob/',views.applyJob,name='apply_job'),
    path('companies_list/',views.company_list,name='companies_list'),
    path('search_company/',views.search_company,name='search_company'),
    path('companies_details/<int:id>/',views.companies_details,name='companies_details'),
    path('search_jobs/',views.search_jobs,name='search_jobs'),
    path('filter_data/',views.filter_data,name='filter_data')

]
