# apps/auditlog/tests/test_api.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.auditlog.models import AuditLog

User = get_user_model()


class AuditLogAPITest(APITestCase):
    def setUp(self):
        # ایجاد کاربر ادمین و لاگین
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="pass1234",
            email="admin@example.com"
        )
        self.client.login(username="admin", password="pass1234")

        # ایجاد یک نمونه اولیه لاگ
        AuditLog.objects.create(
            what="تست API",
            changes={"test": "ok"}
        )

    def test_list_auditlogs(self):
        """
        تست لیست کردن لاگ‌ها از طریق API
        """
        url = reverse('auditlog-list')  # استفاده از نام ViewSet
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # سازگاری با هر دو حالت: با پجینیشن و بدون پجینیشن
        results = response.data
        if isinstance(results, dict) and "results" in results:
            results = results["results"]

        self.assertGreaterEqual(len(results), 1)
