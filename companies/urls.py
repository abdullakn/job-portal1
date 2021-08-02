from django.urls import path
from . import views



urlpatterns = [
    path('add_job/',views.add_jobs,name='add_jobs'),
    path('profile/',views.company_profile,name='company_profile'),
    path('job_list/',views.job_listing,name='view_jobs'),
    path('job_applications/',views.job_applications,name='job_applications'),
    path('delete_job/<int:id>/',views.delete_job,name='delete_job'),
    path('applicant_details/<int:id>/',views.applicant_details,name='applicant_details'),
    path('view_resume/<int:id>/',views.view_resume,name='view_resume'),
    path('job_applicant_view/<int:id>/',views.job_applicant_view,name='job_applicant_view'),
    path('manage_applications/<int:id>/',views.manage_applications,name='manage_applications')

]
