from os import name
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
    path('filter_data/',views.filter_data,name='filter_data'),
    path('view_pdf/<int:id>/',views.view_pdf,name='view_pdf'),
    path('make_cv/',views.cv_management,name='make_cv'),
    path('view_cv/',views.view_cv,name='view_cv'),
    path('employee_badge/<int:id>/',views.employee_badge,name='employee_badge'),
    path('employee_appliedjobs/',views.employee_applied_list,name='employee_appliedjobs'),
    path('favourite_jobs/<int:id>/',views.favourite_jobs,name='favourite_jobs'),
    path('view_favourite/',views.view_favourite,name='view_favourite'),
    path('machine_test/',views.view_machinetest,name='machine_test'),
    path('download_machine_test/<int:id>/',views.download_machinetest,name='download_machinetest'),
    path('propic_save/',views.propic_save,name='propic_save'),
    path('make_coverletter/',views.make_coverletter,name='make_coverletter'),
    path('add_education/',views.add_education,name='add_education'),
    path('add_experience/',views.add_experience,name='add_experience'),
    path('add_skills/',views.add_skills,name='add_skills'),
    path('add_awards/',views.add_awards,name='add_awards'),
    path('saveans/',views.saveans,name='saveans'),
    path('submit_answers',views.submit_answers,name='submit_answers'),
    path('badges/',views.badges,name='badges'),
    path('reply_machine_test/<int:id>/',views.reply_machine_test,name='reply_machine_test'),
    path('delete_machinetest/<int:id>/',views.delete_machinetest,name='delete_machinetest'),
    path('delete_favourite/<int:id>/',views.delete_favourite,name='delete_favourite'),
    path('load_cv/',views.load_cv,name='load_cv'),
    path('delete_education/<int:id>/',views.delete_education,name='delete_education'),
    path('delete_skills/<int:id>/',views.delete_skill,name='delete_skills'),
    path('delete_experience/<int:id>/',views.delete_experience,name='delete_experience'),
    path('delete_awards/<int:id>/',views.delete_awards,name='delete_awards'),
   

]
