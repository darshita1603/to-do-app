from django.contrib import admin
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',views.LoginView,name="login"),
    path('register/',views.RegisterView,name="register"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('profile/',views.profile,name="profile"),
    path('logout/',views.profile,name="logout"),
    path('tasklist/',views.listview,name="tasklist"),
    path('<str:pk>/edit',views.editdata,name="editdata"),
    path('<str:pk>/delete',views.deletedata,name="deletedata"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)