"""
URL configuration for project_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet
from notes.views import NoteViewSet

from tasks.api_views import ProjectViewSet, TaskViewSet
from tasks.urls import TaskList


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register('events', EventViewSet, basename='event')
router.register('notes', NoteViewSet, basename='note')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    # path('api/tasks/', TaskList.as_view(), name='task_list'),
    # path('api/', views.TaskList.as_view(), name='task_list'),
    path('events/', include('events.urls')),
    path('notes/', include('notes.urls')),

# path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
]