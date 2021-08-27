from django.contrib import admin
from django.urls import path
from . import views 
from addtask.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('addtask/',views.addtask,name="addtask"),
     path('taskhistory/',views.TaskHistory,name="taskhistory"),
     path('status/<int:pk>',views.Checkstatus,name="status"),
     path('complete/',views.complete,name="complete"),
     path('pending/',views.pending,name="pending"),
     # path('mailsend/',views.mailsend,name="mailsend"),
     # path('<str:pk>/edit',views.editdata,name="editdata"),
     # path('<str:pk>/delete',views,name="editdata"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)