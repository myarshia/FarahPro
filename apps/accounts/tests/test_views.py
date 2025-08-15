# apps/accounts/tests/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # کاربر عادی
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        # ادمین
        self.admin = User.objects.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass"
        )
        self.list_url = reverse('user-list')
        # کاربر دیگر برای تست
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="otherpass"
        )

    # ------------------ Create ------------------
    def test_create_user_without_authentication(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # ------------------ List ------------------
    def test_list_users_requires_authentication(self):
        response = self.client.get(self.list_url)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # پشتیبانی از هر دو حالت pagination فعال/غیرفعال
        results = response.data
        if isinstance(results, dict) and "results" in results:
            results = results["results"]
        self.assertGreaterEqual(len(results), 1)

    # ------------------ Retrieve ------------------
    def test_retrieve_user_authenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # # پشتیبانی از هر دو حالت pagination فعال/غیرفعال
        # results = response.data
        # if isinstance(results, dict) and "results" in results:
        #     results = results["results"]  # حالا results یک لیست است
        # self.assertEqual(results[0]['username'], self.other_user.username)
        self.assertEqual(response.data['username'], self.other_user.username)

    # ------------------ Update (PUT) ------------------
    def test_update_user_authenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.force_authenticate(user=self.user)
        data = {
            "username": "updatedname",
            "email": self.other_user.email,
            "password": "otherpass"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, "updatedname")

    # ------------------ Partial Update (PATCH) ------------------
    def test_partial_update_user_authenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.force_authenticate(user=self.user)
        data = {"username": "patchedname"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, "patchedname")

    # ------------------ Delete ------------------
    def test_delete_user_requires_admin(self):
        """کاربر غیرادمین نباید کاربر دیگر را حذف کند"""
        url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.force_authenticate(user=self.user)  # غیرادمین
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])
        self.assertTrue(User.objects.filter(pk=self.other_user.pk).exists())

    def test_delete_user_authenticated_admin(self):
        """ادمین می‌تواند کاربر دیگر را حذف کند"""
        url = reverse('user-detail', kwargs={'pk': self.other_user.pk})
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.other_user.pk).exists())
