from django.urls import path
from .views import home, create_project, view_project, edit_project


class TaskList:
    pass


urlpatterns = [
    path('', home, name='home'),
    path('create/', create_project, name='create_project'),
    path('view/<int:pk>/', view_project, name='view_project'),
    path('edit/<int:pk>/', edit_project, name='edit_project'),
    # path('api/tasks/', TaskList.as_view(), name='task_list'),
    # path('projects/<int:project_id>/tasks/<int:task_id>/notes/', create_note, name='create_note'),

    # path()
]

