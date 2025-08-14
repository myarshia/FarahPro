from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.organizations.models import Organization
from django.contrib.auth import get_user_model


class OrganizationAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

    def test_list_organizations(self):
        Organization.objects.create(legal_name="Test Organization")
        url = reverse("organization-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_organization(self):
        url = reverse("organization-list")
        data = {"legal_name": "New Org", "country": "Iran"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
