from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet

router = SimpleRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = router.urls
