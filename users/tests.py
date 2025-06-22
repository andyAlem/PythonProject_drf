from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Тестовый курс", description="Тестовое описание", owner=self.user
        )

    def test_create_course(self):
        """Тестирование создания курса"""
        url = reverse("materials:course-list")
        data = {
            "name": "Тестовый курс",
            "description": "Тестовое описание",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], self.course.name)

    def test_list_courses(self):
        """Тестирование получения списка курсов"""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_retrieve_course(self):
        """Тестирование получения курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.course.name)

    def test_update_course(self):
        """Тестирование обновления курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        data = {"name": "Тестовый курс", "description": "Обновленное описание"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.course.name)

    def test_delete_course(self):
        """Тестирование удаления курса"""
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Тестировние уроков


class LessonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="lessonuser@example.com", password="test"
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="API Course", description="REST", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Intro",
            description="Введение в REST",
            course=self.course,
            owner=self.user,
            video_url="http://youtube.com/video",
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Новый урок",
            "description": "Описание",
            "course": self.course.id,
            "video_url": "http://youtube.com/newvideo",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Новый урок")

    def test_list_lessons(self):
        """Тестирование списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_retrieve_lesson(self):
        """Тестирование получения урока"""
        url = reverse("materials:lessons_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.lesson.name)

    def test_update_lesson(self):
        """Тестирование обновления урока"""
        url = reverse("materials:lessons_update", args=[self.lesson.pk])
        data = {
            "name": "Обновленный урок",
            "description": "UОбновленное описание",
            "video_url": "http://youtube.com/updatedvideo",
            "course": self.course.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Обновленный урок")

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lessons_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# Тестирование подписок


class CourseSubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="test1234"
        )
        self.course = Course.objects.create(
            name="Django", description="Web dev", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve_contains_subscription_flag(self):
        """Проверяем наличие is_subscribed в данных курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])

    def test_subscription_add_and_remove(self):
        """Проверка установки и удаления подписки"""
        url = reverse("materials:subscriptions")

        # Подписка
        response = self.client.post(url, data={"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Повторный запрос (отписка)
        response = self.client.post(url, data={"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscription_without_course_id(self):
        """Ошибка, если course_id не передан"""
        url = reverse("materials:subscriptions")
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
