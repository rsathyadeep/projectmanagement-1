from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Project, Task
from django.utils.timezone import now, timedelta

class ProjectModelTest(TestCase):
    def setUp(self):
        """Set up a user and project for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project.",
            owner=self.user
        )

    def test_project_creation(self):
        """Test that a project can be created successfully."""
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.owner, self.user)

    def test_project_str_representation(self):
        """Test the string representation of the project."""
        self.assertEqual(str(self.project), "Test Project")

class TaskModelTest(TestCase):
    def setUp(self):
        """Set up users, a project, and tasks for testing."""
        self.owner = User.objects.create_user(username='owner', password='testpassword')
        self.assignee = User.objects.create_user(username='assignee', password='testpassword')
        self.collaborator = User.objects.create_user(username='collaborator', password='testpassword')
        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project.",
            owner=self.owner
        )
        self.parent_task = Task.objects.create(
            title="Parent Task",
            description="This is a parent task.",
            status="todo",
            due_date=now().date() + timedelta(days=5),
            assigned_to=self.assignee,
            project=self.project
        )
        self.task = Task.objects.create(
            title="Child Task",
            description="This is a child task.",
            status="in_progress",
            due_date=now().date() + timedelta(days=2),
            assigned_to=self.assignee,
            project=self.project,
            parent_task=self.parent_task
        )
        self.task.collaborators.add(self.collaborator)

    def test_task_creation(self):
        """Test that a task can be created successfully."""
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(self.task.title, "Child Task")
        self.assertEqual(self.task.status, "in_progress")
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.parent_task, self.parent_task)

    def test_task_collaborators(self):
        """Test that collaborators are correctly added to a task."""
        self.assertIn(self.collaborator, self.task.collaborators.all())
        self.assertEqual(self.task.collaborators.count(), 1)

    def test_task_due_date(self):
        """Test that the due date is correctly set."""
        self.assertEqual(self.task.due_date, now().date() + timedelta(days=2))

    def test_task_str_representation(self):
        """Test the string representation of the task."""
        self.assertEqual(str(self.task), "Child Task")

    def test_task_parent_relationship(self):
        """Test that the parent task relationship works."""
        self.assertEqual(self.task.parent_task, self.parent_task)
        self.assertEqual(self.parent_task.task_set.count(), 1)
        self.assertIn(self.task, self.parent_task.task_set.all())
