from django.db import models


class TaskStatus(models.TextChoices):
    TODO = ("todo", "To do")
    DONE = ("done", "Done")


class TaskModel(models.Model):
    id: models.AutoField
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "tasks"
        db_table = "tasks_tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title}: Updated at {self.created_at}"
