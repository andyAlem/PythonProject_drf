from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_forbidden_links


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с курсами"""

    is_subscribed = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с уроками"""

    video_url = serializers.CharField(validators=[validate_forbidden_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации о курсе, включая количества уроков и их список"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "image",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )
