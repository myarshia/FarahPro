# apps/accounts/tests/test_serializers.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_serializer_fields(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertIn("email", data)
        # password نباید خروجی باشد
        self.assertNotIn("password", data)

    def test_serializer_create_user(self):
        serializer = UserSerializer(data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123"
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("newpassword123"))

    def test_serializer_update_user(self):
        serializer = UserSerializer(self.user, data={"username": "updateduser"}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "updateduser")
