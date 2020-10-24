from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import User,Project,UserProjects,Task
from django.db.models import Q,Prefetch
from datetime import datetime
from datetime import date
from django.core.paginator import Paginator
import time
# Create your views here.

def index(request,type_input="cron"):
    # tasks=Task.objects.filter(worker=request.user)
    if request.user.is_authenticated:
        

        tasks=Task.objects.filter(project__worker=request.user,date=date.today()).order_by("date")
        
        for task in tasks:
            if task.date:
                task.date=task.date.strftime("%d/%m/%Y")
            if task.minutes:
                task.time_used=str(int(task.minutes/60))+"h "+str(int(task.minutes%60))+"m"
            
        
        projects_manager=UserProjects.objects.filter(worker=request.user,manager=True,activated=True)
        projects=UserProjects.objects.filter(worker=request.user,manager=False,activated=True)
        
        cron=(type_input=="cron")
        manual=(type_input=="manual") 
        file_type= (type_input=="file") 
        
        return render(request,"timetracker/index.html",{
            "tasks":tasks,
            "projects":projects,
            "projects_manager":projects_manager,
            "manual":manual,
            "cron": cron,
            "file":file_type
        })
    else:
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "timetracker/login.html", {
                "message": "Invalid username and/or password.",
                "login":True
            })
    else:
        return render(request, "timetracker/login.html",{
            "login":True
        })
@csrf_exempt    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "timetracker/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "timetracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "timetracker/register.html",{
            "login":True
        })
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def project_view(request):
    if request.user.is_authenticated:
        users=User.objects.exclude(username=request.user.username)
        projects_manager=Project.objects.filter(manager=request.user)
        projects=UserProjects.objects.filter(worker=request.user,manager=False)
        return render(request, "timetracker/projects.html",{
                "projects_manager":projects_manager,
                "projects":projects,
                "users":users,
                "manager":True
            })        
    else:
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt  
def project(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({"status": 403}, status=403)
        data=json.loads(request.body)['body']
        
        project=Project(manager=request.user,name=data['name'])
        
        for member in data['members']:
            if not User.objects.filter(username=member).exists():
                return JsonResponse({"status": 404,"message":"User does not exist."}, status=404)
        project.save()
        user_project=UserProjects(project=project,worker=request.user,manager=True)
        user_project.save()
        for member in data['members']:
            user_project=UserProjects(project=project,worker=User.objects.get(username=member),manager=False)
            user_project.save()
        return JsonResponse({"status": 200}, status=200)
    else:
        return JsonResponse({"status": 401}, status=401)


@csrf_exempt
def insert_task(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({"status": 403}, status=403)
        
        data=json.loads(request.body)['body']
        
        project_name=data["project_name"].strip()
        content=data["task_content"].strip()
        date=data["date"].strip()
        minutes=data["minutes"]
        
        if project_name=="" or content=="" or date=="" or  minutes==0 or not Project.objects.filter(name=project_name).exists():
           return JsonResponse({"status": 412}, status=412)
        minutes_number=int(minutes)
        
        user_project=UserProjects.objects.get(worker=request.user,project__name=project_name)
        
        
        task=Task(project=user_project,task_content=content,minutes=minutes_number,date=date)
        task.save()
        return JsonResponse({"status": 200}, status=200)
    else:
        return JsonResponse({"status": 401}, status=401)
    
@csrf_exempt
def task_list(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({"status": 403}, status=403)
        date_filter=json.loads(request.body)['body'].lower()


        if date_filter=="today":
            tasks=Task.objects.filter(project__worker=request.user,date=date.today()).order_by("date")
        elif date_filter=="week":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*7*24))).order_by("date")
        elif date_filter=="month":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*24*30))).order_by("date")
        elif date_filter=="year":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*7*24*365))).order_by("date")
        else:
            tasks=Task.objects.filter(project__worker=request.user).order_by("date")
            
        tasks_array=[]
        for task in tasks:
            task_serial={}
            task_serial['date']=task.date.strftime("%d/%m/%Y")
            task_serial['time_used']=str(int(task.minutes/60))+"h "+str(int(task.minutes%60))+"m"
            task_serial['project_name']=task.project.project.name
            task_serial['task_content']=task.task_content
            task_serial['id']=task.id
            tasks_array.append(task_serial)

        
        return JsonResponse({"status": 200,"data":tasks_array}, status=200)
    else:
        return JsonResponse({"status": 401}, status=401)

def edit_task(request,task_id):
    if request.user.is_authenticated and Task.objects.filter(project__worker=request.user,id=task_id).exists():
        
        task=Task.objects.get(project__worker=request.user,id=task_id)
        projects_manager=Project.objects.filter(manager=request.user)
        projects=UserProjects.objects.filter(worker=request.user,manager=False)

        date_formated=(task.date.strftime("%Y-%m-%d"))
        task.hours=int(task.minutes/60)
        task.minutes=int(task.minutes)-task.hours*60
        
        return render(request,"timetracker/editTask.html",{
            "task":task,
            "projects":projects,
            "projects_manager":projects_manager,
            "date_formated":date_formated
        })
        
    else:
        return HttpResponseRedirect(reverse("login"))

def edit_project(request,project_id):
    
    if request.user.is_authenticated and UserProjects.objects.filter(worker=request.user,project__id=project_id).exists():
        
        project=UserProjects.objects.get(worker=request.user,project__id=project_id)
        workers=UserProjects.objects.filter(project__id=project_id).exclude(worker=request.user)
        users=User.objects.exclude(username=request.user.username)
        if project.manager:
            tasks=Task.objects.filter(project__project__id=project_id).order_by("date")
        else:
            tasks=Task.objects.filter(project__worker=request.user,project__project__id=project_id).order_by("date")
        
        

        for task in tasks:
            if task.date:
                task.date=task.date.strftime("%d/%m/%Y")
            if task.minutes:
                task.time_used=str(int(task.minutes/60))+"h "+str(int(task.minutes%60))+"m"
        
        workers_list_compare=[]
        
        for worker in workers:
            workers_list_compare.append(worker.worker)
            
        final_users=[]
        for user in users:
            if user in workers_list_compare:
                user.disabled=True
            final_users.append(user)

        return render(request,"timetracker/editProject.html",{
            "project":project,
            "manager":project.manager,
            "users":final_users,
            "workers":workers,
            "tasks":tasks
        })
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse("project"))
    
    else:
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt
def manage_task(request):
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({"status": 403}, status=403)
        
        data=json.loads(request.body)['body']
        print(data)
        if not Task.objects.filter(project__worker=request.user,id=data["taskid"]).exists():
            return JsonResponse({"status": 401}, status=401)
        
        project_name=data["project_name"].strip()
        content=data["task_content"].strip()
        date=data["date"].strip()
        minutes=data["minutes"]
        user_project=UserProjects.objects.get(worker=request.user,project__name=project_name)
        minutes_number=int(minutes)
        
        if data["option"]=="delete":
            Task.objects.filter(project__worker=request.user,id=data["taskid"]).delete()
        elif data["option"]=="save":
            task=Task.objects.filter(project__worker=request.user,id=data["taskid"]).update(project=user_project,task_content=content,minutes=minutes_number,date=date)
        else:
            return JsonResponse({"status": 500}, status=500)
            
        return JsonResponse({"status": 200,"data":data}, status=200)
    else:
        return HttpResponseRedirect(reverse("login"))
@csrf_exempt
def manage_project(request):
    
    if request.user.is_authenticated:
        if request.method != "POST":
            return JsonResponse({"status": 403}, status=403)
        
        data=json.loads(request.body)['body']
        if not Project.objects.filter(manager=request.user,id=data["projectid"]).exists():
            return JsonResponse({"status": 401}, status=401)
        
        project_name=data["name"].strip()
        projectid=data['projectid']
        
        user_project=UserProjects.objects.get(worker=request.user,project__id=projectid)

    
        
        if data["option"]=="delete":
            
            Project.objects.filter(manager=request.user,id=data["projectid"]).delete()
            UserProjects.objects.filter(project__manager=request.user,project__id=data["projectid"]).delete()
            Task.objects.filter(project__project__manager=request.user,project__project__id=data["projectid"]).delete()
        elif data["option"]=="save":
            Project.objects.filter(manager=request.user,id=data["projectid"]).update(name=project_name)
            UserProjects.objects.filter(project__manager=request.user,project__id=data["projectid"]).update(activated=False)
        else:
            return JsonResponse({"status": 500}, status=500)
            
        return JsonResponse({"status": 200,"data":data}, status=200)
    else:
        return HttpResponseRedirect(reverse("login"))