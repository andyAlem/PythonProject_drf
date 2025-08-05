from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Полная информация о пользователе"""

    class Meta:
        model = User
        fields = "__all__"


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class PaymentSerializer(ModelSerializer):
    """Сериализатор для работы с оплатами"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["user", "stripe_session_id", "stripe_url"]
