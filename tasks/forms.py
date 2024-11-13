from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'assigned_to']

# class NoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = ['content','title', 'status', 'due_date', 'project']