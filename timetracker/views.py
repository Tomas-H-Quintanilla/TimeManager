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
    """Returns the main page.

    Args:
        type_input (str, optional): Type of input form choosen. Defaults to "cron".
    """
    
    # tasks=Task.objects.filter(worker=request.user)
    if request.user.is_authenticated:
        

        tasks=Task.objects.filter(project__worker=request.user,date=date.today()).order_by("-date")
        
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
        name= request.POST['name']
        surname= request.POST['surname']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "timetracker/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,name=name,surname=surname)
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
                "users":users
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
        
        if data['type']=='csv':
            valid_data=False
            objects_insert=[]
            for readed_data in data['content']:
                
                divided_data=readed_data.strip().split("\n")
                for set_results in divided_data:
                    set_results=set_results.split(",")
                    if len(set_results)==len(data['order']):
                        count=0
                        valid_data=True
                        object_insert={}
                        while count<(len(set_results)):
                            
                            object_insert[data['order'][count]]=set_results[count]
                            count=count+1
                            
                        objects_insert.append(object_insert)
                        
            for object_task in objects_insert:
                user_project=UserProjects.objects.get(worker=request.user,project__name=object_insert['project'].strip())
                
                if not object_insert['hours'].strip():
                    object_insert['hours']='0'
                if not object_insert['minutes'].strip():
                    object_insert['minutes']='0'
                
                
                
                minutes=int(float(object_insert['hours'])*60)+int(object_insert['minutes'])
                
                object_insert['date']=object_insert['date'].replace("/","-")
                if not len(object_insert['date'].split("-")[0])==4:
                    date_frags=object_insert['date'].split("-")
                    
                    object_insert['date']="-".join((date_frags[2],date_frags[1],date_frags[0]))
                
                task=Task(project=user_project,task_content=object_insert['task'],minutes=minutes,date=object_insert['date'].replace("/","-"))
                task.save()
            
            if not valid_data:
                
                return JsonResponse({"status": 412}, status=412)
        else:
            
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
            tasks=Task.objects.filter(project__worker=request.user,date=date.today()).order_by("-date")
        elif date_filter=="week":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*7*24))).order_by("-date")
        elif date_filter=="month":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*24*30))).order_by("-date")
        elif date_filter=="year":
            tasks=Task.objects.filter(project__worker=request.user,date__gte=(datetime.fromtimestamp(time.time()-3600*7*24*365))).order_by("-date")
        else:
            tasks=Task.objects.filter(project__worker=request.user).order_by("-date")
            
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

def profile_view(request):
    if request.user.is_authenticated:
        users=User.objects.exclude(username=request.user.username)
        projects_manager=Project.objects.filter(manager=request.user)
        projects=UserProjects.objects.filter(worker=request.user,manager=False)
        return render(request, "timetracker/profile.html",{
                "projects_manager":projects_manager,
                "projects":projects,
                "users":users
            })    
    else:
        return HttpResponseRedirect(reverse("login"))


def modify_profile(request):
    
    if request.user.is_authenticated:
        if request.method != "POST":
            return HttpResponseRedirect(reverse("profile"))
        
        fields={}
        
        if request.POST["username"]!='':
            fields['username']=request.POST["username"]
        else:
            fields['username']=request.user.username
        
        if request.POST["email"]!='':
            fields['email']=request.POST["email"]
        else:
            fields['email']=request.user.email
        
        if request.POST["name"]!='':
            fields['name']=request.POST["name"]
        else:
            fields['name']=request.user.name
        
        if request.POST["surname"]!='':
            fields['surname']=request.POST["surname"]
        else:
            fields['surname']=request.user.surname

        # Ensure password matches confirmation

        User.objects.filter(username=request.user.username).update(surname=fields['surname'],
                                                                   name=fields['name'],
                                                                   email=fields['email'],
                                                                   username=fields['username']
                                                                   )
        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password!='':
            if password!=confirmation:
                return render(request, "timetracker/profile.html", {
                    "message": "Passwords must match."
                    })
            
            else:
                User.objects.filter(username=request.user.username).update(password=password)
        
        return HttpResponseRedirect(reverse("profile"))
        
        
    else:
        return HttpResponseRedirect(reverse("login"))