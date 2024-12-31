
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from .models import Project, Task

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.user
        )

    def test_project_creation(self):
        """Test that a project can be created with valid data"""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.description, 'Test Description')
        self.assertEqual(self.project.owner, self.user)

    def test_project_str_method(self):
        """Test the string representation of a project"""
        self.assertEqual(str(self.project), 'Test Project')

class TaskModelTests(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(username='owner', password='pass123')
        self.assignee = User.objects.create_user(username='assignee', password='pass123')
        self.collaborator = User.objects.create_user(username='collaborator', password='pass123')
        
        # Create project
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.owner
        )
        
        # Create a task
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='todo',
            due_date=date.today() + timedelta(days=7),
            assigned_to=self.assignee,
            project=self.project
        )

    def test_task_creation(self):
        """Test that a task can be created with valid data"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.status, 'todo')
        self.assertEqual(self.task.assigned_to, self.assignee)
        self.assertEqual(self.task.project, self.project)

    def test_task_str_method(self):
        """Test the string representation of a task"""
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_status_choices(self):
        """Test that task status must be one of the defined choices"""
        valid_statuses = ['todo', 'in_progress', 'done']
        for status in valid_statuses:
            self.task.status = status
            self.task.save()
            self.assertEqual(self.task.status, status)

    def test_task_with_parent_task(self):
        """Test creating a task with a parent task"""
        child_task = Task.objects.create(
            title='Child Task',
            description='Child Description',
            status='todo',
            project=self.project,
            parent_task=self.task
        )
        self.assertEqual(child_task.parent_task, self.task)

    def test_task_collaborators(self):
        """Test adding collaborators to a task"""
        self.task.collaborators.add(self.collaborator)
        self.assertIn(self.collaborator, self.task.collaborators.all())

    def test_optional_fields(self):
        """Test that optional fields can be null/blank"""
        optional_task = Task.objects.create(
            title='Optional Fields Task',
            description='Test Description',
            status='todo',
            project=self.project
        )
        self.assertIsNone(optional_task.due_date)
        self.assertIsNone(optional_task.assigned_to)
        self.assertIsNone(optional_task.parent_task)
        self.assertEqual(optional_task.collaborators.count(), 0)

    def test_cascade_delete_project(self):
        """Test that deleting a project deletes its tasks"""
        self.project.delete()
        self.assertEqual(Task.objects.filter(id=self.task.id).count(), 0)

    def test_set_null_on_user_delete(self):
        """Test that deleting an assigned user sets task's assigned_to to null"""
        self.assignee.delete()
        self.task.refresh_from_db()
        self.assertIsNone(self.task.assigned_to)



                #########################################################################################################
                #       VIEWS TEST CASES                                                                                #
                #########################################################################################################

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectAPITests(APITestCase):
    def setUp(self):
        # Create a minimal valid project using actual model fields
        self.project = Project.objects.create()  # Add required fields here
        self.valid_update_data = {}  # Add valid fields for your Project model
        
    def test_get_projects_list(self):
        """
        Test retrieving list of projects
        """
        url = reverse('project-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_get_project_detail(self):
        """
        Test retrieving a specific project
        """
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.project.id)
    
    def test_update_project(self):
        """
        Test updating a project via PUT
        """
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.put(url, self.valid_update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()

class TaskAPITests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create()  # Add required fields here
        
        # Create a minimal valid task
        self.task = Task.objects.create(
            project=self.project
            # Add other required fields here
        )
        self.valid_update_data = {
            'project': self.project.id
            # Add other valid fields for your Task model
        }
        
    def test_get_tasks_list(self):
        """
        Test retrieving list of tasks
        """
        url = reverse('task-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_get_task_detail(self):
        """
        Test retrieving a specific task
        """
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.id)
    
    def test_update_task(self):
        """
        Test updating a task via PUT
        """
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.put(url, self.valid_update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()