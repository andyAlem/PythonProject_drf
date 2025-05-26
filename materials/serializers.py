from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Payment


class CourseSerializer(ModelSerializer):
    """Сериализатор для работы с курсами"""

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """Сериализатор для работы с уроками"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для отображения информации о курсе, включая количества уроков и их список"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "image", "description", "lessons_count", "lessons")
