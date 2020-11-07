
from django.urls import path
from . import views



urlpatterns = [
    path("",views.index,name="index"),
    path("index/<str:type_input>",views.index,name="index"),
    path("index",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("project",views.project_view,name="project"),
    path("projectSave",views.project,name="project_save"),
    path("insert_task",views.insert_task,name="insert_task"),
    path("task_list",views.task_list,name="task_list"),
    path("edit_task/<int:task_id>",views.edit_task,name="edit_task"),
    path("edit_project/<int:project_id>",views.edit_project,name="edit_project"),
    path("manage_task",views.manage_task,name="manage_task"),
    path("manage_project",views.manage_project,name="manage_project"),
    path("profile",views.profile_view,name="profile"),
    path("modify_profile",views.modify_profile,name="modify_profile"),
    path("download_tasks",views.download_tasks,name="download_tasks"),
    path("manager",views.manager,name="manager")
]