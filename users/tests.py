from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):
    """ Класс для тестирования работы с пользователями """

    # def setUp(self):

    def test_user_create(self):
        """ Тестирование создания нового пользователя """

        url = reverse("users:register")
        data = {
            "email": "test_user@test.com",
            "password": "123456"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "test_user@test.com")
