from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Project(models.Model):
    manager=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=128)

class UserProjects(models.Model):
    manager=models.BooleanField(default=False)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    worker=models.ForeignKey(User, on_delete=models.CASCADE)
    activated=models.BooleanField(default=True)

class Task(models.Model):
    task_content=models.CharField(max_length=128)
    project=models.ForeignKey(UserProjects,on_delete=models.CASCADE)
    date=models.DateTimeField(null=True)
    minutes=models.IntegerField(null=True)
    