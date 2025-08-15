# apps/accounts/tests/test_api.py

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="user@example.com",
            password="pass12345"
        )

    def test_list_users_requires_auth(self):
        """لیست کاربران فقط برای کاربران لاگین کرده"""
        url = reverse("user-list")
        response = self.client.get(url)
        # self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_list_users_authenticated(self):
        """لیست کاربران با احراز هویت"""
        self.client.force_authenticate(self.user)
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # پشتیبانی از هر دو حالت pagination فعال/غیرفعال
        results = response.data
        if isinstance(results, dict) and "results" in results:
            results = results["results"]
        self.assertGreaterEqual(len(results), 1)

    def test_create_user(self):
        """ساخت کاربر جدید"""
        url = reverse("user-list")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "pass123456",
            "first_name": "New",
            "last_name": "User"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
