from django.conf import settings
from django.db import models

from common.models.abstract_base_model import AbstractBaseModel


class TaskStatus(models.TextChoices):
    TODO = ("todo", "To do")
    DONE = ("done", "Done")


class TaskModel(AbstractBaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    class Meta:  # pyright: ignore
        app_label = "tasks"
        db_table = "tasks_tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title}: Updated at {self.created_at}"
