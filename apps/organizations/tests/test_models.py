from django.test import TestCase
from apps.organizations.models import Organization

class OrganizationModelTest(TestCase):
    def test_create_organization(self):
        org = Organization.objects.create(
            legal_name="Test Organization",
            trade_name="Test Org",
            country="Iran",
            city="Tehran"
        )
        self.assertEqual(str(org), "Test Organization")
        self.assertTrue(org.is_active)
