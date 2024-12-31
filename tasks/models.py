from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


# class User(models.Model):
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#
#     def __str__(self):
#         return self.username

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ])
    due_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    parent_task = models.ForeignKey('task', on_delete=models.SET_NULL, null=True, blank=True)
    collaborators = models.ManyToManyField(User, related_name='task_collaborations', blank=True)
    # Collaborators = models.ManyToManyField(User)

    def __str__(self):
        return self.title

# class Note(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     status = models.CharField(max_length=50)
#     due_date = models.DateField(null=True, blank=True)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.title
#




