from rest_framework import routers

from accounts.views import AuthCheckView, AuthView

router = routers.SimpleRouter()
router.register(r"auth", AuthView, basename="auth")
router.register(r"", AuthCheckView, basename="auth-check")

urlpatterns = router.urls
