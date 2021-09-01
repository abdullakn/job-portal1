from django.urls import path
from . import views



urlpatterns = [
    path('add_job/',views.add_jobs,name='add_jobs'),
    path('edit_job/<int:id>/',views.edit_job,name='edit_job'),
    path('profile/',views.company_profile,name='company_profile'),
    path('job_list/',views.job_listing,name='view_jobs'),
    path('job_applications/',views.job_applications,name='job_applications'),
    path('delete_job/<int:id>/',views.delete_job,name='delete_job'),
    path('applicant_details/<int:id>/',views.applicant_details,name='applicant_details'),
    path('view_resume/<int:id>/',views.view_resume,name='view_resume'),
    path('job_applicant_view/<int:id>/',views.job_applicant_view,name='job_applicant_view'),
    path('manage_applications/<int:id>/',views.manage_applications,name='manage_applications'),
    path('download_zip/<int:id>/',views.download_zip,name='download_zip'),
    path('add_gallery/',views.add_gallery,name='add_gallery'),
    path('add_extra_company/',views.add_extra_company,name='add_extra_company'),
    path('add_subscription/',views.add_subscription,name='add_subscription'),
    path('checkout_session/',views.checkout_session,name='checkout_session'),
    path('checkout_session_golden/',views.checkout_session_golden,name='checkout_session_golden'),
    path('checkout_session_premium/',views.checkout_session_premium,name='checkout_session_premium'),
    path('pay_success/',views.pay_success,name='pay_success'),
    path('pay_cancel/',views.pay_cancel,name='pay_cancel')

]
