from django.contrib import admin
from django.contrib import admin
from .models import Note
# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_by', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)