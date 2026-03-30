from django.contrib import admin
from .models import Project, Task, Sprint, ActivityLog, Notification


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by', 'created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'priority', 'project', 'assigned_to']


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'project', 'start_date', 'end_date']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read']