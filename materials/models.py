from django.db import models


class Course(models.Model):
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

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
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
    )

    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Добавьте ссылку на видео"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
