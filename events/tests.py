from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event
from django.utils.timezone import now, timedelta

class EventModelTest(TestCase):
    def setUp(self):
        # Create a user to associate with the event
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.start_date = now()
        self.end_date = self.start_date + timedelta(hours=2)

    def test_event_creation(self):
        """Test that an event can be created successfully."""
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            start_date=self.start_date,
            end_date=self.end_date,
            location="Test Location",
            created_by=self.user,
        )
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.created_by, self.user)

    def test_event_str_representation(self):
        """Test the string representation of the event."""
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            start_date=self.start_date,
            end_date=self.end_date,
            location="Test Location",
            created_by=self.user,
        )
        self.assertEqual(str(event), "Test Event")

    def test_created_at_and_updated_at_auto_fields(self):
        """Test that created_at and updated_at are set correctly."""
        event = Event.objects.create(
            title="Test Event",
            description="This is a test event.",
            start_date=self.start_date,
            end_date=self.end_date,
            location="Test Location",
            created_by=self.user,
        )
        self.assertIsNotNone(event.created_at)
        self.assertIsNotNone(event.updated_at)

        # Ensure updated_at changes on save
        old_updated_at = event.updated_at
        event.title = "Updated Test Event"
        event.save()
        self.assertNotEqual(event.updated_at, old_updated_at)

    def test_start_date_before_end_date(self):
        """Test that the start date is before the end date."""
        with self.assertRaises(ValueError):
            Event.objects.create(
                title="Invalid Event",
                description="This is an invalid event.",
                start_date=self.end_date,
                end_date=self.start_date,  # Invalid: start_date is after end_date
                location="Test Location",
                created_by=self.user,
            )

    def test_blank_location(self):
        """Test that location can be blank."""
        event = Event.objects.create(
            title="No Location Event",
            description="This event has no location.",
            start_date=self.start_date,
            end_date=self.end_date,
            location="",  # Blank location
            created_by=self.user,
        )
        self.assertEqual(event.location, "")

    def test_event_required_fields(self):
        """Test that required fields must be provided."""
        with self.assertRaises(ValueError):
            Event.objects.create(
                description="Missing title and dates.",
                created_by=self.user,
            )
