from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_user(self):
        """ساخت کاربر معمولی"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpass123",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("strongpass123"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        """ساخت سوپر یوزر"""
        admin = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_is_unique(self):
        """ایمیل باید یکتا باشد"""
        User.objects.create_user(username="testuser", email="unique@example.com", password="123")
        with self.assertRaises(Exception):
            User.objects.create_user(username="testuser", email="unique@example.com", password="456")
