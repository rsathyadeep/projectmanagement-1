from django.contrib import admin
from django.contrib import admin
from .models import Event
# Register your models here.


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'created_by')
    list_filter = ('start_date', 'created_by')
    search_fields = ('title', 'description')
    ordering = ('-start_date',)