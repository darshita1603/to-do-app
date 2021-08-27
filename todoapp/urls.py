from django.contrib import admin
from django.urls import path
from . import views 
from.views import TaskDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.LoginView,name="login"),
    path('register/',views.RegisterView,name="register"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('profile/',views.profile,name="profile"),
    path('logout/',views.logout,name="logout"),
    path('tasklist/',views.listview,name="tasklist"),
    path('csvfile/',views.csvfile,name="csvfile"),
    path('<str:pk>/mailsend',views.mailsend,name="mailsend"),
    path('<str:pk>/downloadpdf',views.downloadpdf,name="downloadpdf"),
    path('<str:pk>/edit',views.editdata,name="editdata"),
    path('<str:pk>/delete',TaskDeleteView.as_view(),name="task-delete"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)