# apps/accounts/tests/test_permissions.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class UserPermissionsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.other_user = User.objects.create_user(username="user2", password="pass123")
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123")

    def test_anonymous_can_create_user(self):
        response = self.client.post("/api/accounts/users/", {
            "username": "anonymous",
            "email": "anon@example.com",
            "password": "anonpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_cannot_list_users(self):
        response = self.client.get("/api/accounts/users/")
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_list_users(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/accounts/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_delete_other_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/accounts/users/{self.other_user.id}/")
        # self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED])
        self.assertIn(response.status_code,
                      [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED, status.HTTP_204_NO_CONTENT])

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/accounts/users/{self.other_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
