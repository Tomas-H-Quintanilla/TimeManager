from django.contrib import admin
from .models import User,Project,UserProjects,Task
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(UserProjects)
admin.site.register(Task)