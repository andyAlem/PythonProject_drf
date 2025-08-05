from django.urls import reverse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.pagination import CustomPagination
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer)
from materials.services.stripe_service import (create_checkout_session,
                                               create_stripe_price,
                                               create_stripe_product)
from materials.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner
from users.serializers import PaymentSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(ModelViewSet):
    """Класс для работы с курсами"""

    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def get_serializer_class(self):
        """Получение сериализатора для определенного курса и вложенных уроков"""
        if self.action == "retrieve":
            return CourseDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Права доступа для модераторов"""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve", "partial_update"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    pagination_class = CustomPagination

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        course_id = self.get_object().id
        send_course_update_email.delay(course_id)
        return response


class LessonCreateApiView(CreateAPIView):
    """Класс для создания урока"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Класс для получения списка уроков"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Класс для получения одного урока"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    """Класс для обновления урока"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    """Класс для удаления урока"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModer,
    )


class SubscriptionAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        user = request.user

        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "Не передан course_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class StripePaymentView(APIView):
    """Класс для оплаты курса"""

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(user=request.user)

        product = create_stripe_product(payment.paid_course.name)
        price = create_stripe_price(product["id"], payment.amount)

        success_url = (
            request.build_absolute_uri(reverse("materials:payment-success"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        )
        cancel_url = request.build_absolute_uri(reverse("materials:payment-cancel"))

        session = create_checkout_session(price["id"], success_url, cancel_url)

        payment.stripe_session_id = session["id"]
        payment.stripe_url = session["url"]
        payment.save()

        return Response(
            {"payment_id": payment.id, "stripe_url": payment.stripe_url},
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
def payment_success(request):
    return Response({"message": "Оплата прошла успешно!"})


@api_view(["GET"])
def payment_cancel(request):
    return Response({"message": "Оплата отменена"})
