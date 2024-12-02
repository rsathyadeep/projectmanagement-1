from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note
from datetime import timedelta

class NoteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='12345'
        )

    def test_create_note(self):
        note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            created_by=self.user
        )
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note.')
        self.assertEqual(note.created_by, self.user)
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)

    def test_note_str_representation(self):
        note = Note.objects.create(
            title='Another Test Note',
            content='This is another test note.',
            created_by=self.user
        )
        self.assertEqual(str(note), 'Another Test Note')

    def test_note_update(self):
        note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            created_by=self.user
        )
        created_at = note.created_at
        note.content = 'Updated test note.'
        note.save()
        updated_note = Note.objects.get(pk=note.pk)
        self.assertEqual(updated_note.content, 'Updated test note.')
        self.assertGreater(updated_note.updated_at, created_at)

    def test_note_delete(self):
        note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            created_by=self.user
        )
        note_id = note.pk
        note.delete()
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=note_id)