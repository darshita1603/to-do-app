
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django_tables2.utils import A
from. models import Registration
from django_tables2.config import RequestConfig
from django.urls import reverse_lazy
from django_tables2 import SingleTableView
import re
from django.template.loader import get_template
from .utils import render_to_pdf 
from django import forms
import pandas as pd
import django_tables2 as tables
import reportlab 
from reportlab.pdfgen import canvas
from .models import *
from .email import send_email
from .tables import PersonTable
# from django.contrib.auth.forms import UserUpdateForm
from addtask.forms import UserUpdateForm
from django.views.generic import DeleteView
from.filter import ProductFilter
from django.http import HttpRequest,HttpResponse, request,HttpResponseRedirect

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
pat = re.compile(reg)

createdate=[] 
enddate=[]
createtime=[]
endtime=[]
nametask=[]
username=[]

def LoginView(request):
    if request.session.has_key('user_id'):
         return redirect('dashboard') 
    else:
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
                # print(request.session['user_id'])
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
    print(uid)
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
    print("hiii")
    del request.session['user_id']
    return redirect('login')
    

# class PersonListView(SingleTableView):
#     model = AddTask
#     table_class = PersonTable
#     template_name = 'tasklist.html'

def listview(request):
    if request.session.has_key('user_id'):
        uid = request.session['user_id']
        data = Registration.objects.get(pk=uid)
        # print(request.GET, "lllllll")
        # data_list=AddTask.objects.all()
        # print(data_list,"yyyyyyy")
        task_qs=AddTask.objects.filter(user=uid,complete=False)
        filter_data= ProductFilter(request.GET, queryset=task_qs)
        # list_view=AddTask.objects.filter(complete=False)
        print(filter_data,"hiiiiii")
        table_data=PersonTable(filter_data.qs)

        # print(table_data,"jjjjj") 
        paginate = {'per_page': 5, 'page': 1}
        RequestConfig(request,paginate).configure(table_data)

        context={
            "table_data":table_data,
            "data":data,
            "filter_data":filter_data
        }

        # for i in data_list:
        #     createdate.append(i.create_date)
        #     print(i.end_date)
        #     enddate.append(i.end_date)
        #     createtime.append(i.create_time)
        #     nametask.append(i.name_of_task)
        #     endtime.append(i.end_time)
        #     # username.append(i.user)
        #     # print(i.user,"hhhhhhkkkkk")

        #     # print(i.create_date,"kkkkk")
            
        # dict={'Name of task':nametask,'Create date':createdate,'End date':enddate,'Create time':createtime,'End time':endtime}
        # df = pd.DataFrame(dict)
        # df.to_csv(r'F:\Django\to-do-app\tests.csv')
        return render(request,"tasklist.html",context)
    else:
        return redirect('login')

def editdata(request,pk):
    if request.session.has_key('user_id'):
        uid = request.session['user_id']
        data = Registration.objects.get(pk=uid)
        data_list = get_object_or_404(AddTask, pk=pk)
        print(data_list,"uuuuuuuuuuuuu")
        form = UserUpdateForm(request.POST or None, instance=data_list)

        # for i in form:
        #     print(i.user,"jijiiiji")
        print(form,"iiiiiiiiiiii")
        if form.is_valid():
            print("*"*100)
            form.save()
            form=UserUpdateForm(request.POST)
            return redirect("tasklist")
        return render(request,'tasks/edittask.html',{"form":form,'data':data})
    else:
        return redirect('login')


# def deletedata(request,pk):
#     uid = request.session['user_id']
#     data = Registration.objects.get(pk=uid)
#     data_list = get_object_or_404(AddTask, pk=pk)
#     if request.method =="GET":
#         print("hii")
#         data_list.delete()
#         return redirect("tasklist")
#     return render(request,'tasks/deletetask.html',{'data':data})

class TaskDeleteView(DeleteView):
    model = AddTask
    success_url = reverse_lazy('tasklist')

def csvfile(request):
    if request.session.has_key('user_id'):
        print("jjjjjj")
        uid = request.session['user_id']
        data = Registration.objects.get(pk=uid)
        data_list=AddTask.objects.all()
        for i in data_list:
            createdate.append(i.create_date)
            enddate.append(i.end_date)
            createtime.append(i.create_time)
            nametask.append(i.name_of_task)
            endtime.append(i.end_time) 
                      
        dict={'Name of task':nametask,'Create date':createdate,'End date':enddate,'Create time':createtime,'End time':endtime}
        df = pd.DataFrame(dict)
        # p='F:\Django\to-do-app\'
        # df.to_csv("./dataset/file'+str(i)+'.csv',index=False) 
        # filename="results"+str(date)+".csv"'
        a= df.to_csv(r'F:\Django\to-do-app\data.csv')
        return render(request,'todoapp/addtask_csv.html',{'data':data},a)
    else:
        return redirect('login')
    
def downloadpdf(request,pk):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    pdf=AddTask.objects.get(pk=pk)
    print(pdf,"jjjjj")
    # context={'pdf':pdf}
    # pdf_data = render_to_pdf('tasks/downloadfile.html',context)
    # p = canvas.Canvas('1.pdf')
    # p.drawString(200, 200, 'hiii') 
    # p.showPage()  
    # p.save()    
    return render(request,"tasks/downloadpdf.html",{'data':data,'pdf':pdf})
    # return HttpResponse(pdf_data, content_type='application/pdf')

# def mailsend(request,pk):
#     uid = request.session['user_id']
#     data = Registration.objects.get(pk=uid)
#     pdf=AddTask.objects.get(pk=pk)
#     context={'pdf':pdf}
#     pdf_data = render_to_pdf('tasks/downloadfile.html',context)
#     return HttpResponse(pdf_data, content_type='application/pdf')

def mailsend(request,pk):
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    print(data,"hiiiiiiiiiiiiii")
    pdf=AddTask.objects.get(pk=pk)
    context={'pdf':pdf}
    render_to_pdf('tasks/downloadfile.html',context)
    send_email(pdf)
    return redirect('downloadpdf',pk=pk)
    # return render(request,"tasks/downloadfile.html")
