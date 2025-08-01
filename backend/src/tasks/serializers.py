from rest_framework import serializers

from tasks.models import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:  # pyright: ignore
        model = TaskModel
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
