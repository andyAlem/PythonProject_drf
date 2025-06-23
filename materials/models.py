from django.db import models

from users.models import User


class Course(models.Model):
    """Класс курса"""

    name = models.CharField(
        max_length=150, verbose_name="Курс", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="materials/images",
        verbose_name="Превью",
        help_text="Добавьте превью",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание"
    )

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор"
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", default=0
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Класс урока"""

    name = models.CharField(
        max_length=150, verbose_name="Урок", help_text="Укажите название урока"
    )
    image = models.ImageField(
        upload_to="materials/images",
        verbose_name="Превью",
        help_text="Добавьте превью",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Укажите описание"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
        related_name="lessons",
    )

    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Добавьте ссылку на видео"
    )

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Подписка на курс"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} Вы подписаны на курс: {self.course}"
