from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer

from common.authentications import IsAuthenticated
from tasks.models import TaskModel
from tasks.serializers import TaskSerializer


@extend_schema(
    tags=["Tasks"],
)
class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()
    http_method_names = ["delete", "get", "patch", "post"]

    def get_queryset(self) -> QuerySet[TaskModel]:
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer: BaseSerializer) -> None:
        serializer.save(user=self.request.user)
