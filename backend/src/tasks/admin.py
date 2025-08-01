from django.contrib import admin

from tasks.models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin[TaskModel]):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("title", "created_at", "updated_at")
    search_fields = ["title", "description"]
