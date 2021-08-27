
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from todoapp. models import *
import django_tables2 as tables
from django.http import HttpRequest,HttpResponse, request,HttpResponseRedirect
from .tables import CompleteTable, CompleteTask, PendingTask

def addtask(request):
    print("hyyyyy")
    print(request.method)
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    task_qs=AddTask.objects.filter(user=uid)
    print(task_qs)
    if request.method=='POST':
        print("yyyyy")
        obj=AddTask()
        # u_id=request.POST['uid']
        # print(u_id,"kk")

        obj.user=Registration.objects.get(pk=uid)
        # print(obj.user,"jjjjjjj")
        # u_id=request.POST['uid']
        # print(u_id)
        obj.name_of_task=request.POST['taskname']
        # print(taskname)
        obj.details=request.POST['details']
        obj.create_date=request.POST['sdate']
        obj.end_date=request.POST['edate']
        obj.create_time=request.POST['stime']
        obj.end_time=request.POST['etime']
        obj.save()
        # AddTask(user_id=u_id).save()
        messages.success(request,'Hey your task is add')
        return redirect('tasklist')
    return render(request,"tasks/addtask.html",{'data':data})

def Checkstatus(request,pk):
    task=AddTask.objects.get(pk=pk)
    # breakpoint()
    task.complete=True
    task.save()
    return redirect('taskhistory')


def TaskHistory(request): 
    uid = request.session['user_id']
    data = Registration.objects.get(pk=uid)
    data_list=AddTask.objects.filter(user=uid,complete=True).all() 
    list_view=data_list
    table_data=CompleteTable(list_view)

    return render(request,"tasks/taskhistory.html",{'table_data':table_data,'data':data})

def downloadpdf(request):
     return render(request,"tasks/taskhistory.html")


def complete(request):
    uid = request.session['user_id']
    print(uid,"hhhhhhhhhhhhhhh")
    data = Registration.objects.get(pk=uid)
    data_list=AddTask.objects.filter(user=uid,complete=True).all() 
    list_view=data_list
    table_data=CompleteTask(list_view)
    return render(request,"tasks/completetask.html",{'table_data':table_data,'data':data})

def pending(request):
    uid = request.session['user_id']
    print(uid,"hhhhhhhhhhhhhhh")
    data = Registration.objects.get(pk=uid)
    data_list=AddTask.objects.filter(user=uid,complete=False).all() 
    list_view=data_list
    table_data=PendingTask(list_view)
    return render(request,"tasks/pendingtask.html",{'table_data':table_data,'data':data})

# def mailsend(request,pk):
#     uid = request.session['user_id']
#     data = Registration.objects.get(pk=uid)
#     pdf=AddTask.objects.get(pk=pk)
#     context={'pdf':pdf}
#     pdf_data = render_to_pdf('tasks/downloadfile.html',context)
#     return HttpResponse(pdf_data, content_type='application/pdf')
#     # return render(request,"tasks/downloadfile.html")

# def sendpdf(request,pk):
#     uid = request.session['user_id']
#     data = Registration.objects.get(pk=uid)
#     pdf=AddTask.objects.get(pk=pk)
#     context={'pdf':pdf}
#     pdf_data = render_to_pdf('tasks/downloadfile.html',context)
#     return HttpResponse(pdf_data, content_type='application/pdf')