from django.urls import path
from . import views



urlpatterns = [

  path('login/',views.login,name='superadmin_login'),
  path('home/',views.superadmin_home,name='superadmin_home'),
  path('view_user/',views.view_users,name='view_users'),
  path('view_companies/',views.view_companies,name='view_companies'),
  path('view_jobs/',views.view_jobs,name='see_jobs'),
  path('view_applications/',views.view_applications,name='see_applications'),
  path('table/',views.tables,name='table'),
  path('add_category/',views.add_category,name='add_category'),
  path('add_questions/<int:id>/',views.add_questions,name='add_questions'),

]