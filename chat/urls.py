
from django.urls import path
from . import views


urlpatterns = [
   
    path('',views.messages_pages,name='messages_page'),
    path('create_thread/',views.create_thread,name='create_thread')
]