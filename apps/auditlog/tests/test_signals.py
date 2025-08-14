from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.auditlog.models import AuditLog
from apps.organizations.models import Organization

User = get_user_model()

class AuditLogSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="signaltester",
            password="pass1234",
            email="signal@example.com"
        )

        # داده‌های پیش‌فرض برای ساخت Organization
        self.org_defaults = {
            "legal_name": "Test Organization Legal",
            "trade_name": "Test Org",
            "country": "Iran",
            "city": "Tehran",
        }

    def test_create_organization_logs_audit(self):
        org = Organization.objects.create(**self.org_defaults)

        logs = AuditLog.objects.filter(what__contains="Organization ایجاد شد")
        self.assertEqual(logs.count(), 1)
        self.assertIn(self.org_defaults["legal_name"], str(logs.first().changes))

    def test_update_organization_logs_audit(self):
        org = Organization.objects.create(**self.org_defaults)
        org.legal_name = "Updated Organization Legal"
        org.save()

        logs = AuditLog.objects.filter(what__contains="Organization ویرایش شد")
        self.assertGreaterEqual(logs.count(), 1)
        self.assertIn("Updated Organization Legal", str(logs.last().changes))

    def test_delete_organization_logs_audit(self):
        org = Organization.objects.create(**self.org_defaults)
        org.delete()

        logs = AuditLog.objects.filter(what__contains="Organization حذف شد")
        self.assertEqual(logs.count(), 1)
        self.assertIn(self.org_defaults["legal_name"], str(logs.first().changes))
