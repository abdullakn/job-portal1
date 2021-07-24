from django.urls import path
from . import views



urlpatterns = [
    path('add_job/',views.add_jobs,name='add_jobs'),
    path('profile/',views.company_profile,name='company_profile'),
    path('job_list/',views.job_listing,name='view_jobs'),
    # path('job_view/',views.job_view,name='job_view')

]
