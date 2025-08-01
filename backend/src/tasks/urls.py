from rest_framework import routers

from tasks.views import TaskViewSet

router = routers.SimpleRouter()
router.register("", TaskViewSet, basename="tasks")

urlpatterns = router.urls
