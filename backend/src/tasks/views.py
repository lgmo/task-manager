from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from tasks.models import TaskModel
from tasks.serializers import TaskSerializer


@extend_schema(
    tags=["Tasks"],
)
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()
    http_methods = ["delete", "get", "patch", "post"]
