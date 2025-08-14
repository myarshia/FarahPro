from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.auditlog.models import AuditLog

User = get_user_model()

class AuditLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="pass1234",
            email="tester@example.com"
        )

    def test_create_auditlog(self):
        log = AuditLog.objects.create(
            who=self.user,
            what="ایجاد تست",
            changes={"field": "value"}
        )
        self.assertEqual(log.who, self.user)
        self.assertEqual(log.what, "ایجاد تست")
        self.assertIsNotNone(log.when)
        self.assertEqual(log.changes, {"field": "value"})
