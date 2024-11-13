from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import ProjectForm, TaskForm
from .models import User, Project, Task
from django.contrib.auth.decorators import login_required, login_not_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

@login_required
def home(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'tasks/home.html', {'projects': projects})


@login_required
def create_task(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('view_project', pk=pk)
    else:
        form = TaskForm(initial={'status': 'todo'})

    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'tasks/create_project.html', {'form': form})

@login_required
def view_project(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = Task.objects.filter(project=project)
    return render(request, 'tasks/view_project.html', {'project': project, 'tasks': tasks})

@login_required
def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('view_project', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/edit_project.html', {'form': form})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class TaskList(APIView):
    def GET(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def POST(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

