from django.contrib import admin
from .models import User, Project, Task
from django.contrib import admin
# from .models import Note
admin.site.site_header = "Project Management Admin"
admin.site.site_title = "Project Management Admin Portal"
admin.site.index_title = "Welcome to the Project Management Administration"

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    search_fields = ('title',)
    list_filter = ('owner__username',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'project')
    list_filter = ('status', 'project__title')

# @admin.register(Note)
# class NoteAdmin(admin.ModelAdmin):
#     list_display = ('title', 'status', 'due_date', 'project','content')
#     list_filter = ('due_date','project')
#     search_fields = ('title',)
#     date_hierarchy = 'due_date'