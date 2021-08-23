
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from todoapp. models import *
import django_tables2 as tables
from django.http import HttpRequest,HttpResponse, request,HttpResponseRedirect
from .tables import CompleteTable

def addtask(request):
    print("hyyyyy")
    print(request.method)
    
    if request.method=='POST':
        print("yyyyy")
        u_id=request.POST['uid']
        print(u_id)
        taskname=request.POST['taskname']
        details=request.POST['details']
        s_date=request.POST['sdate']
        e_date=request.POST['edate']
        s_time=request.POST['stime']
        e_time=request.POST['etime']

        AddTask(user_id=u_id,name_of_task=taskname,details=details,create_date=s_date,end_date=e_date,create_time=s_time,end_time=e_time).save()
        messages.success(request,'Hey your task is add')
        return redirect('tasklist')
    return render(request,"tasks/addtask.html")

def Checkstatus(request,pk):
    task=AddTask.objects.get(pk=pk)
    # breakpoint()
    task.complete=True
    task.save()
    return redirect('taskhistory')


def TaskHistory(request): 
    data=AddTask.objects.filter(complete=True).all()
    # print(AddTask.objects.filter(complete=True))  
    list_view=data
    table_data=CompleteTable(list_view)

    return render(request,"tasks/taskhistory.html",{'table_data':table_data})