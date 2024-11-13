from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# class NoteViewSet(viewsets.ModelViewSet):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
