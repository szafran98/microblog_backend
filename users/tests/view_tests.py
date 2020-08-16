import json

from django.contrib.auth import get_user_model
from users.models import CustomUser
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {'username': 'testuser', 'email': 'test@mail.com', 'password': 'pass'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.first().username, 'testuser')

    def test_registration_no_data(self):
        data = {}
        response = self.client.post('/api/users', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)


class LoginTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@mail.com',
            password='pass'
        )

    def test_user_login(self):
        data = {'username': 'test@mail.com', 'password': 'pass'}
        response = self.client.post('/api/auth/', data)
        self.assertEqual(response.data['token'], Token.objects.get(user=self.user).key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_no_user(self):
        data = {'username': 'bad@mail.com', 'password': 'pas'}
        response = self.client.post('/api/auth/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
