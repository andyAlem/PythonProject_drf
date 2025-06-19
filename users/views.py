from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsModer
from users.serializers import (PaymentSerializer, UserReadSerializer,
                               UserSerializer)


class PaymentViewSet(ModelViewSet):
    """Единый класс для работы с платежами"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("date",)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff or IsModer().has_permission(self.request, self):
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)


class UserViewSet(ModelViewSet):
    """CRUD для пользователей"""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только текущий пользователь
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserReadSerializer
        return UserSerializer


class UserCreateApiView(CreateAPIView):
    """Эндпоинт для регистрации"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()
        user_group, _ = Group.objects.get_or_create(name="users")
        user.groups.add(user_group)
