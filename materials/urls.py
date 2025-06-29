from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    StripePaymentView,
    SubscriptionAPIView,
    payment_cancel,
    payment_success,
)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
    # Подписка на курс
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
    # Оплата
    path("create-payment/", StripePaymentView.as_view(), name="create-stripe-payment"),
    path("payment-success/", payment_success, name="payment-success"),
    path("payment-cancel/", payment_cancel, name="payment-cancel"),
]

urlpatterns += router.urls
