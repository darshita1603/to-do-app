from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django_tables2.utils import A
from. models import Registration
from django_tables2 import SingleTableView
import re
from django import forms
import django_tables2 as tables
from .models import *
from .tables import PersonTable
# from django.contrib.auth.forms import UserUpdateForm
from addtask.forms import UserUpdateForm
from django.views.generic import DeleteView
from.filter import ProductFilter
from django.http import HttpRequest,HttpResponse, request,HttpResponseRedirect

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
pat = re.compile(reg)
      
def LoginView(request):
    if request.method=='POST':
        loginname=request.POST['username']
        loginpassword=request.POST['userpassword']
        user=Registration.objects.get(username=loginname)

        u_name=user.username
        u_pass=user.password

        # username = request.session['']
        if u_name ==loginname and u_pass==loginpassword:
            # request.session['user_id'] = Registration.objects.filter(username=loginname).values_list('id')
            r = list(Registration.objects.filter(username=loginname).values_list('id',flat=True))
            request.session['user_id']=r[0]
            print(request.session['user_id'])
            # print(request.session['user_id'])
            return redirect('dashboard') 
        else:
            messages.error(request,f'Please check UserName Or Password')
            return redirect('login')

    return render(request,'auth-login.html')

def RegisterView(request):
    if request.method=='POST':
        useremail=request.POST['useremail']
        username=request.POST['username']
        userpassword=request.POST['userpassword']

        if len(username)> 12:
            print("hii")
            messages.error(request,"USername must be under 12 characters")
            return redirect('register')

        if not username.isalnum():
            print("msg")
            messages.error(request,"USername should only contain letters and numbers")
            return redirect('register')

        if not (re.fullmatch(regex, useremail)):
           messages.error(request,"Email is not Valid")
           return redirect('register')

        mat = re.search(pat, userpassword)

        if not mat:
           messages.error(request,"Password is not Valid")
           return redirect('register')
        
        Registration(username=username,email=useremail,password=userpassword).save()
        messages.success(request,f'Account created for {username}')
        return redirect('login')
    else:
        return render(request,'auth-register.html')

def dashboard(request):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    return render(request,'dashboard.html',{'data':data})

def profile(request):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
   
    if request.method=='POST':
        u_name=request.POST.get('name')
        u_image=request.FILES.get('image')
        u_email=request.POST.get('email')
        u_mobileno=request.POST.get('mobileno')
        u_about=request.POST.get('about')
        u_dof=request.POST.get('dateofbirth')


        if u_image is None:
            u_image=data.image
            print(u_image)

        data.username=u_name
        data.mobileno=u_mobileno
        data.email=u_email  
        data.about=u_about
        data.dateofbirth=u_dof
        data.image=u_image
        data.save()

    return render(request,"profile.html",{"data":data})

def logout(request):
    pass

# class PersonListView(SingleTableView):
#     model = AddTask
#     table_class = PersonTable
#     template_name = 'tasklist.html'

def listview(request):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    filter_data= ProductFilter(request.GET, queryset=AddTask.objects.all())
    list_view=AddTask.objects.filter(complete=False)
    table_data=PersonTable(list_view) 
    # breakpoint()

    # if table_data.complete==True:
    #     data=AddTask.objects.filter(complete=True)
    #     data.delete()
    # else:
    #     print("jj")
    # uid = request.session['user_id']
    # data = Registration.objects.get(pk=uid)
    return render(request,"tasklist.html",{'table_data':table_data,"data":data,"filter_data":filter_data})

def editdata(request,pk):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    data_list = get_object_or_404(AddTask, pk=pk)
    form = UserUpdateForm(request.POST or None, instance=data_list)
    if form.is_valid():
        form.save()
        form=UserUpdateForm(request.POST)
        return redirect("tasklist")
    return render(request,'tasks/edittask.html',{"form":form,'data':data})

def deletedata(request,pk):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    data_list = get_object_or_404(AddTask, pk=pk)
    if request.method =="GET":
        print("hii")
        data_list.delete()
        return redirect("tasklist")
        

    return render(request,'tasks/deletetask.html',{'data':data})


