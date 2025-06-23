from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Course, Lesson
from users.models import Payment, User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(
            name="Python Pro", description="Advanced Python", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Advanced Python",
            description="Advanced Python",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование получения курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("name"), self.course.name)

    def test_course_create(self):
        """Тестирование создания курса"""
        url = reverse("materials:course-list")
        data = {
            "name": "Python Pro",
            "description": "Advanced Python",
        }
        response = self.client.post(url, data=data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


####### Оплата
